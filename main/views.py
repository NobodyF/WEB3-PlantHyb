from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from .forms import PlantForm
from .forms import ContactForm
from django.contrib import messages
from .serializers import PlantSerializer
from rest_framework import generics
from web3 import Web3
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import HybridForm
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
import requests
from django.db import transaction
from django.contrib.auth import logout as django_logout
from django.core.serializers import serialize 
import random
import string


def base(request):
    try:
        if request.user.is_authenticated:
            context = {
            }
            return render(request, 'main/smain.html', context)
        else:
            context = {
            }
            return render(request, 'main/smain.html', context)
    except:
        context = {
        }
        return render(request, 'main/smain.html', context)
    

def checklogin(request):
    try: user = request.POST['text']
    except: user = ""
    try: password = request.POST['password']
    except: password = ""

    user = authenticate(request, username=user, password=password)

    if user is not None:
        login(request, user)

    return HttpResponseRedirect(reverse('main:base'))

def logout_one(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:base'))

def home(request):
    
    return render(request, 'main/smain.html')


@login_required
def hybridizations(request):
    plants = Plant.objects.all()
    return render(request, 'main/hybridizations.html', {'plants': plants})

@login_required
def plants(request):
    plants = Plant.objects.all()
    for plant in plants:
        plant.lower_name = plant.plant_name.lower()
    return render(request, 'main/plants.html', {'plants': plants})


from web3 import Web3
import web3
import os


from eth_utils import to_checksum_address
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper functions to retrieve environment variables
def get_alchemy_url():
    return os.getenv('ALCHEMY_URL')

def get_contract_address():
    return to_checksum_address(os.getenv('CONTRACT_ADDRESS'))

def get_private_key():
    return os.getenv('PRIVATE_KEY')

def get_eth_address():
    return os.getenv('ETH_ADDRESS')

def get_contract_abi():
    return [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "hybridId",
                    "type": "uint256"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                }
            ],
            "name": "HybridRegistered",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "plantId",
                    "type": "uint256"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                }
            ],
            "name": "PlantRegistered",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "hybridId",
                    "type": "uint256"
                },
                {
                    "internalType": "string",
                    "name": "hybridName",
                    "type": "string"
                }
            ],
            "name": "registerHybrid",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "plantId",
                    "type": "uint256"
                },
                {
                    "internalType": "string",
                    "name": "plantName",
                    "type": "string"
                }
            ],
            "name": "registerPlant",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "hybridId",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "transferHybridOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "plantId",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address"
                }
            ],
            "name": "transferPlantOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "hybrids",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "hybridId",
                    "type": "uint256"
                },
                {
                    "internalType": "string",
                    "name": "hybridName",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "plants",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "plantId",
                    "type": "uint256"
                },
                {
                    "internalType": "string",
                    "name": "plantName",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

def get_web3_instance():
    alchemy_url = get_alchemy_url()
    return Web3(Web3.HTTPProvider(alchemy_url))

def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, owner=request.user)

        if form.is_valid():
            try:
                plant = form.save(commit=False)
                plant_name = form.cleaned_data['plant_name']
                plant.owner = request.user  
                plant.save()

                # Create contract instance and call registerPlant function
                w3 = get_web3_instance()
                contract_address = get_contract_address()
                contract_abi = get_contract_abi()

                plant_contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)
                plant_id = int(plant.id)
                nonce = w3.eth.get_transaction_count(get_eth_address())
                tx_data = plant_contract_instance.encodeABI(
                    fn_name="registerPlant",
                    args=[plant_id, plant_name]
                )
                gas_price = w3.eth.gas_price
                gas_limit = 1000000  # some random test gas limit
                transaction = {
                    'to': contract_address,
                    'value': 0,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                    'data': tx_data,
                }
                private_key = get_private_key()
                signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                # Convert tx_hash to string before saving
                tx_hash_str = tx_hash.hex()

                # Save transaction hash along with plant details
                PlantTransaction.objects.create(
                    plant=plant,
                    tx_hash=tx_hash_str
                )

                return redirect('main:plants')
            except Exception as e:
                error_message = f"Failed to register plant on the blockchain: {str(e)}"
                print(error_message)
                return HttpResponse(error_message)
    else:
        form = PlantForm()
    return render(request, 'main/add_plant.html', {'form': form})


@login_required
def profile(request):
    user_plants = Plant.objects.filter(owner=request.user)
    plant_transactions = PlantTransaction.objects.filter(plant__in=user_plants)
    
    user_hybrids = Hybrid.objects.filter(owner=request.user)
    hybrid_transactions = HybridTransaction.objects.filter(hybrid__in=user_hybrids)
    
    return render(request, 'main/profile.html', {'plant_transactions': plant_transactions, 'hybrid_transactions': hybrid_transactions})




@login_required
def perform_hybridization(request):
    if request.method == 'POST':
        parent1_id = request.POST.get('parent1')
        parent2_id = request.POST.get('parent2')
        
        
       
        
        # Redirect to hybridization results with the newly created hybrid's parent IDs
        return redirect('main:hybridization_results',parent1_id=parent1_id,parent2_id=parent2_id)

    plants = Plant.objects.all()
    return render(request, 'main/hybridizations.html', {'plants': plants})

from .models import Plant, Hybrid, HybridTransaction
@login_required
def hybridization_results(request, parent1_id=None, parent2_id=None):
    if request.method == 'POST':
        form = HybridForm(request.POST, owner=request.user)

        if form.is_valid():
            try:
                # Save hybrid information to the database
                hybrid = form.save(commit=False)
                hybrid_name = form.cleaned_data['hybrid_name']
                hybrid.hybrid_name = hybrid_name
                
                hybrid.is_hybrid = True  # Mark as hybrid TODO:
                hybrid.owner = request.user  

                hybrid.save()

                # Create contract instance and call registerHybrid function
                w3 = get_web3_instance()
                contract_address = get_contract_address()
                contract_abi = get_contract_abi()
                hybrid_contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)
                hybrid_id = int(hybrid.id)
                nonce = w3.eth.get_transaction_count(get_eth_address())
                tx_data = hybrid_contract_instance.encodeABI(
                    fn_name="registerHybrid",
                    args=[hybrid_id, hybrid_name]
                )
                gas_price = w3.eth.gas_price
                gas_limit = 1000000  # You may need to adjust this value
                transaction = {
                    'to': contract_address,
                    'value': 0,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                    'data': tx_data,
                }
                private_key = get_private_key()
                signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                # Convert tx_hash to string before saving
                tx_hash_str = tx_hash.hex()

                # Save transaction hash along with hybrid details
                HybridTransaction.objects.create(
                    hybrid=hybrid,
                    tx_hash=tx_hash_str
                )

                return redirect('main:hybrids')
            except Exception as e:
                error_message = f"Failed to register hybrid on the blockchain: {str(e)}"
                print(error_message)
                return HttpResponse(error_message)
        else:
             return JsonResponse({'errors': form.errors})
    else:
        try:
            parent1 = Plant.objects.get(id=parent1_id)
            parent2 = Plant.objects.get(id=parent2_id)
            
            # Prepare JSON data for parent plants
            parent1_data = {'id': parent1.id, 'plant_name': parent1.plant_name}
            parent2_data = {'id': parent2.id, 'plant_name': parent2.plant_name}

            for field in parent1._meta.fields:
                field_name = field.name
                field_value = getattr(parent1, field_name)
                parent1_data[field_name] = field_value

            for field in parent2._meta.fields:
                field_name = field.name
                field_value = getattr(parent2, field_name)
                parent2_data[field_name] = field_value

            # Remove 'owner' field from JSON data if necessary
            parent1_data.pop('owner', None)
            parent2_data.pop('owner', None)

            parent1_json = json.dumps(parent1_data, indent=2)
            parent2_json = json.dumps(parent2_data, indent=2)

            form = HybridForm(initial={'parent1': parent1, 'parent2': parent2})
        except Plant.DoesNotExist:
            return HttpResponse("One or more selected plants do not exist.")

    return render(request, 'main/hybridization_results.html', {
        'form': form, 
        'parent1_id': parent1_id, 
        'parent2_id': parent2_id,
        'parent1_json': parent1_json, 
        'parent2_json': parent2_json
    })

@login_required
def hybrids(request):
    hybrids = Hybrid.objects.all()
    return render(request, 'main/hybrids.html', {'hybrids': hybrids})

@login_required
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('main:contact_us')  
    else:
        form = ContactForm()

    return render(request, 'main/smain.html', {'form': form})

class PlantList(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    # blockchain testing TODO:





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # success page, or return JSON response
            return redirect('success_url_name')
        else:
            # Return an error message
            return render(request, 'main/login.html', {'error_message': 'Invalid credentials'})
    else:
        # render the login page
        return render(request, 'main/login.html')
    


API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImM3MmU5MTM4LTcxYmUtNDA0NC04NDEwLThhN2UzYWU0MDhhZiIsIm9yZ0lkIjoiMzgwMjIwIiwidXNlcklkIjoiMzkwNjk0IiwidHlwZUlkIjoiZGZkZmIzYjEtZGE2ZC00ZjJhLWFiOWItYmFjM2M3ZTA3YTQyIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MDkwNTEwNTAsImV4cCI6NDg2NDgxMTA1MH0.wlDNetT8kvGmfRKblVkIaV58m25pxVPxT8TJZni1QoM'
if API_KEY == 'WEB3_API_KEY_HERE':
    print("API key is not set")
    raise SystemExit
def plant_hybridization(request):
    return render(request, 'main/login.html', {})
def my_profile(request):
    return render(request, 'main/profile.html', {})
def request_message(request):
    data = json.loads(request.body)
    print(data)

#setting request expiration time to 1 minute after the present->
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "defi.finance",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "https://defi.finance/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})
    return JsonResponse(json.loads(x.text))

def verify_message(request):
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))
  


def staff_member_required(view_func):

    def _checklogin(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('main:home')  
        return view_func(request, *args, **kwargs)
    return _checklogin

#@staff_member_required

def generate_random_id():
    characters = string.digits  # Use only digits
    random_id = ''.join(random.choices(characters, k=5))
    return random_id

import json

@login_required
def show_plant_details(request, plant_id):
    try:
        plant = Plant.objects.get(id=plant_id)
        plant_data = {}
        for field in plant._meta.fields:
            field_name = field.name
            field_value = getattr(plant, field_name)

            # Convert User object to string representation
            if field_name == 'owner':
                field_value = str(field_value)

            plant_data[field_name] = field_value

        json_data = json.dumps(plant_data, indent=2)
        return HttpResponse(json_data, content_type='application/json')
    except Plant.DoesNotExist:
        return JsonResponse({'error': 'Plant not found'}, status=404)
    
# WHITE version FIXME:

# def show_plant_details(request, plant_id):
#     try:
#         plant = Plant.objects.get(id=plant_id)
#         plant_data = {
#             'id': plant.id,
#             'plant_name': plant.plant_name,
#             'plant_description': plant.plant_description,
#             # Include other fields as needed
#         }
#         # Convert plant_data dictionary to a JSON string with indentation for better readability
#         json_data = json.dumps(plant_data, indent=4)

#         # Create HTML content to display JSON data in a preformatted block
#         html_content = f'<pre>{json_data}</pre>'

#         return HttpResponse(html_content)
#     except Plant.DoesNotExist:
#         return HttpResponse('<p>Plant not found</p>', status=404)
    