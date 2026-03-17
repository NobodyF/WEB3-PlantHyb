import os
import json
import random
import string
from datetime import datetime, timedelta, timezone

import requests
from decouple import config  # FIXED: use decouple, not os.getenv directly
from dotenv import load_dotenv
from eth_utils import to_checksum_address
from web3 import Web3

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rest_framework import generics

from .forms import PlantForm, ContactForm, HybridForm
from .models import Plant, Hybrid, PlantTransaction, HybridTransaction
from .serializers import PlantSerializer

# ---------------------------------------------------------------------------
# Load .env once at module level
# ---------------------------------------------------------------------------
load_dotenv()


# ---------------------------------------------------------------------------
# FIXED: All secrets read from environment — never hardcoded
# ---------------------------------------------------------------------------
def get_alchemy_url():
    return config('ALCHEMY_URL')

def get_contract_address():
    return to_checksum_address(config('CONTRACT_ADDRESS'))

def get_private_key():
    return config('PRIVATE_KEY')

def get_eth_address():
    return config('ETH_ADDRESS')

def get_moralis_api_key():
    # FIXED: was hardcoded JWT in source — now read from .env
    return config('MORALIS_API_KEY')


# ---------------------------------------------------------------------------
# FIXED: ABI moved to a helper — consider putting this in a separate
# abi.json file later (load with json.load) to keep views.py readable
# ---------------------------------------------------------------------------
def get_contract_abi():
    return [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "uint256", "name": "hybridId", "type": "uint256"},
                {"indexed": True, "internalType": "address",  "name": "owner",    "type": "address"}
            ],
            "name": "HybridRegistered",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "uint256", "name": "plantId", "type": "uint256"},
                {"indexed": True, "internalType": "address",  "name": "owner",   "type": "address"}
            ],
            "name": "PlantRegistered",
            "type": "event"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "hybridId",   "type": "uint256"},
                {"internalType": "string",  "name": "hybridName", "type": "string"}
            ],
            "name": "registerHybrid",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "plantId",   "type": "uint256"},
                {"internalType": "string",  "name": "plantName", "type": "string"}
            ],
            "name": "registerPlant",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "hybridId", "type": "uint256"},
                {"internalType": "address", "name": "newOwner", "type": "address"}
            ],
            "name": "transferHybridOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "plantId",  "type": "uint256"},
                {"internalType": "address", "name": "newOwner", "type": "address"}
            ],
            "name": "transferPlantOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "hybrids",
            "outputs": [
                {"internalType": "address",  "name": "owner",      "type": "address"},
                {"internalType": "uint256",  "name": "hybridId",   "type": "uint256"},
                {"internalType": "string",   "name": "hybridName", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "plants",
            "outputs": [
                {"internalType": "address",  "name": "owner",     "type": "address"},
                {"internalType": "uint256",  "name": "plantId",   "type": "uint256"},
                {"internalType": "string",   "name": "plantName", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]


def get_web3_instance():
    return Web3(Web3.HTTPProvider(get_alchemy_url()))


# ---------------------------------------------------------------------------
# Shared blockchain helper — FIXED: extracted duplicate tx logic into one fn
# ---------------------------------------------------------------------------
def _send_blockchain_transaction(fn_name, args):
    """
    Builds, signs, and sends a transaction to the plant registry contract.
    Returns the tx hash as a hex string, or raises on failure.
    """
    w3               = get_web3_instance()
    contract_address = get_contract_address()
    contract         = w3.eth.contract(address=contract_address, abi=get_contract_abi())
    eth_address      = get_eth_address()

    nonce     = w3.eth.get_transaction_count(eth_address)
    gas_price = w3.eth.gas_price
    tx_data   = contract.encodeABI(fn_name=fn_name, args=args)

    # FIXED: estimate gas instead of hardcoding 1_000_000
    gas_estimate = contract.functions[fn_name](*args).estimate_gas(
        {'from': eth_address}
    )
    gas_limit = int(gas_estimate * 1.2)  # 20 % buffer

    raw_tx = {
        'to':       contract_address,
        'value':    0,
        'gas':      gas_limit,
        'gasPrice': gas_price,
        'nonce':    nonce,
        'data':     tx_data,
    }
    signed  = w3.eth.account.sign_transaction(raw_tx, get_private_key())
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def base(request):
    # FIXED: removed pointless if/else that did the same thing both branches
    return render(request, 'main/smain.html', {})


def home(request):
    return render(request, 'main/smain.html')


def checklogin(request):
    # FIXED: use .get() instead of bare try/except to swallow KeyError
    username = request.POST.get('text', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    return HttpResponseRedirect(reverse('main:base'))


def logout_one(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:base'))


def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user     = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:base')  # FIXED: was 'success_url_name' (broken)
        return render(request, 'main/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'main/login.html')


@login_required
def plants(request):
    plants = Plant.objects.all()
    for plant in plants:
        plant.lower_name = plant.plant_name.lower()
    return render(request, 'main/plants.html', {'plants': plants})


@login_required
def hybridizations(request):
    plants = Plant.objects.all()
    return render(request, 'main/hybridizations.html', {'plants': plants})


@login_required
def hybrids(request):
    hybrids = Hybrid.objects.all()
    return render(request, 'main/hybrids.html', {'hybrids': hybrids})


@login_required
def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, owner=request.user)
        if form.is_valid():
            try:
                plant           = form.save(commit=False)
                plant.owner     = request.user
                plant.save()

                # FIXED: uses shared helper instead of duplicated tx code
                tx_hash = _send_blockchain_transaction(
                    fn_name='registerPlant',
                    args=[int(plant.id), plant.plant_name]
                )
                PlantTransaction.objects.create(plant=plant, tx_hash=tx_hash)
                messages.success(request, f'Plant registered on blockchain. Tx: {tx_hash}')
                return redirect('main:plants')

            except Exception as e:
                # FIXED: show error in template via messages, not raw HttpResponse
                messages.error(request, f'Blockchain registration failed: {e}')
                return render(request, 'main/add_plant.html', {'form': form})
    else:
        form = PlantForm()
    return render(request, 'main/add_plant.html', {'form': form})


@login_required
def perform_hybridization(request):
    if request.method == 'POST':
        parent1_id = request.POST.get('parent1')
        parent2_id = request.POST.get('parent2')
        return redirect('main:hybridization_results',
                        parent1_id=parent1_id,
                        parent2_id=parent2_id)
    plants = Plant.objects.all()
    return render(request, 'main/hybridizations.html', {'plants': plants})


@login_required
def hybridization_results(request, parent1_id=None, parent2_id=None):
    if request.method == 'POST':
        form = HybridForm(request.POST, owner=request.user)
        if form.is_valid():
            try:
                hybrid            = form.save(commit=False)
                hybrid.hybrid_name = form.cleaned_data['hybrid_name']
                hybrid.is_hybrid  = True
                hybrid.owner      = request.user
                hybrid.save()

                # FIXED: uses shared helper
                tx_hash = _send_blockchain_transaction(
                    fn_name='registerHybrid',
                    args=[int(hybrid.id), hybrid.hybrid_name]
                )
                HybridTransaction.objects.create(hybrid=hybrid, tx_hash=tx_hash)
                messages.success(request, f'Hybrid registered on blockchain. Tx: {tx_hash}')
                return redirect('main:hybrids')

            except Exception as e:
                messages.error(request, f'Blockchain registration failed: {e}')
                return render(request, 'main/hybridization_results.html', {'form': form})
        return JsonResponse({'errors': form.errors}, status=400)

    # GET — load both parent plants
    try:
        parent1 = Plant.objects.get(id=parent1_id)
        parent2 = Plant.objects.get(id=parent2_id)
    except Plant.DoesNotExist:
        messages.error(request, 'One or more selected plants do not exist.')
        return redirect('main:hybridizations')

    def plant_to_dict(plant):
        data = {}
        for field in plant._meta.fields:
            if field.name == 'owner':
                continue  # FIXED: skip owner instead of pop() after the fact
            data[field.name] = getattr(plant, field.name)
        return data

    form = HybridForm(initial={'parent1': parent1, 'parent2': parent2})
    return render(request, 'main/hybridization_results.html', {
        'form':        form,
        'parent1_id':  parent1_id,
        'parent2_id':  parent2_id,
        'parent1_json': json.dumps(plant_to_dict(parent1), indent=2),
        'parent2_json': json.dumps(plant_to_dict(parent2), indent=2),
    })


@login_required
def profile(request):
    user_plants       = Plant.objects.filter(owner=request.user)
    plant_transactions = PlantTransaction.objects.filter(plant__in=user_plants)
    user_hybrids       = Hybrid.objects.filter(owner=request.user)
    hybrid_transactions = HybridTransaction.objects.filter(hybrid__in=user_hybrids)
    return render(request, 'main/profile.html', {
        'plant_transactions':  plant_transactions,
        'hybrid_transactions': hybrid_transactions,
    })


@login_required
def show_plant_details(request, plant_id):
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        return JsonResponse({'error': 'Plant not found'}, status=404)

    data = {}
    for field in plant._meta.fields:
        value = getattr(plant, field.name)
        data[field.name] = str(value) if field.name == 'owner' else value
    return JsonResponse(data, json_dumps_params={'indent': 2})


@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent!')
            return redirect('main:contact_us')
    else:
        form = ContactForm()
    return render(request, 'main/smain.html', {'form': form})


# ---------------------------------------------------------------------------
# Moralis Web3 auth — FIXED: API key now from .env
# ---------------------------------------------------------------------------
def request_message(request):
    data    = json.loads(request.body)
    present = datetime.now(timezone.utc)
    expiry  = str((present + timedelta(minutes=1)).isoformat()[:-6]) + 'Z'

    response = requests.post(
        'https://authapi.moralis.io/challenge/request/evm',
        json={
            'domain':         'defi.finance',
            'chainId':        1,
            'address':        data['address'],
            'statement':      'Please confirm',
            'uri':            'https://defi.finance/',
            'expirationTime': expiry,
            'notBefore':      '2020-01-01T00:00:00.000Z',
            'timeout':        15,
        },
        headers={'X-API-KEY': get_moralis_api_key()},  # FIXED
    )
    return JsonResponse(response.json())


def verify_message(request):
    data     = json.loads(request.body)
    response = requests.post(
        'https://authapi.moralis.io/challenge/verify/evm',
        json=data,
        headers={'X-API-KEY': get_moralis_api_key()},  # FIXED
    )
    if response.status_code == 201:
        eth_address = response.json().get('address')
        user, _ = User.objects.get_or_create(
            username=eth_address,
            defaults={'is_staff': False, 'is_superuser': False}
        )
        if user.is_active:
            login(request, user)
            request.session['auth_info']    = data
            request.session['verified_data'] = response.json()
            return JsonResponse({'user': user.username})
        return JsonResponse({'error': 'account disabled'}, status=403)
    return JsonResponse(response.json(), status=response.status_code)


# ---------------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------------
class PlantList(generics.ListCreateAPIView):
    queryset         = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Plant.objects.all()
    serializer_class = PlantSerializer