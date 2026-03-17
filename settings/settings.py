"""
Django settings for plant_hybridization project.
"""
import os
from pathlib import Path
from decouple import config  # single source — no need for dotenv separately

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security — all secrets from .env, never hardcoded
# ---------------------------------------------------------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG       = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'main.apps.MainConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"

# ---------------------------------------------------------------------------
# Database — SQLite for local dev, swap DATABASE_URL for prod
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Ethereum / Web3 — FIXED: contract address moved out of source code
# NOTE: ABI for the Transactions contract kept here for reference,
#       but the PlantRegistry ABI lives in views.py / get_contract_abi()
#       Consider moving both ABIs to main/abi.json in Phase 2.
# ---------------------------------------------------------------------------
ETHEREUM_NODE_URL          = config('ALCHEMY_URL')
ETHEREUM_CONTRACT_ADDRESS  = config('CONTRACT_ADDRESS')   # FIXED: was hardcoded

ETHEREUM_CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "from",      "type": "address"},
            {"indexed": False, "internalType": "address", "name": "receiver",  "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount",    "type": "uint256"},
            {"indexed": False, "internalType": "string",  "name": "message",   "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"indexed": False, "internalType": "string",  "name": "account",   "type": "string"},
            {"indexed": False, "internalType": "string",  "name": "keyword",   "type": "string"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "getAllTransactions",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "sender",    "type": "address"},
                    {"internalType": "address", "name": "receiver",  "type": "address"},
                    {"internalType": "uint256", "name": "amount",    "type": "uint256"},
                    {"internalType": "string",  "name": "message",   "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "string",  "name": "account",   "type": "string"},
                    {"internalType": "string",  "name": "keyword",   "type": "string"},
                ],
                "internalType": "struct Transactions.TransferStruct[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getTransactionCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address payable", "name": "receiver", "type": "address"},
            {"internalType": "uint256",          "name": "amount",   "type": "uint256"},
            {"internalType": "string",           "name": "message",  "type": "string"},
            {"internalType": "string",           "name": "account",  "type": "string"},
            {"internalType": "string",           "name": "keyword",  "type": "string"},
        ],
        "name": "transfer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]