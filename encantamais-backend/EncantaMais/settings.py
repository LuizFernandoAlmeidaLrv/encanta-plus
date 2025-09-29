"""
Django settings for EncantaMais project.
"""

from pathlib import Path
import os
# import pymysql # REMOVIDO: Não é mais necessário para PostgreSQL
import dj_database_url
from dotenv import load_dotenv
import logging # Adicionado para configuração de logging

# Carrega .env da raiz do projeto (onde está manage.py)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Corrige erro do MySQLdb quando usa PyMySQL # REMOVIDO: Não é mais necessário para PostgreSQL
# pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Configurações de Segurança
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

print("DEBUG: settings.py está sendo carregado...") # DEBUG: Ponto de verificação

# =========================
# Configuração Database
# =========================
if os.getenv("DATABASE_URL"):
    # Render → Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=60,
            ssl_require=True,
        )
    }
    print("DEBUG: Configuração de banco de dados para PostgreSQL (Render) carregada.") # DEBUG: Ponto de verificação
else:
    # Local → MySQL (ou SQLite como fallback)
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "CONN_MAX_AGE": 60,
        }
    }
    print("DEBUG: Configuração de banco de dados local carregada.") # DEBUG: Ponto de verificação

# =========================
# CORS e Media
# =========================
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT", "media"))
print("DEBUG: Configurações de CORS e Media carregadas.") # DEBUG: Ponto de verificação

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "core",
    "produtos",
    "preco",
    "suprimentos",
    "vendas",
    "financeiro",
]
print("DEBUG: INSTALLED_APPS carregado.") # DEBUG: Ponto de verificação

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
print("DEBUG: MIDDLEWARE carregado.") # DEBUG: Ponto de verificação

ROOT_URLCONF = "EncantaMais.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
print("DEBUG: TEMPLATES carregado.") # DEBUG: Ponto de verificação

WSGI_APPLICATION = "EncantaMais.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
print("DEBUG: AUTH_PASSWORD_VALIDATORS carregado.") # DEBUG: Ponto de verificação

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
print("DEBUG: REST_FRAMEWORK carregado.") # DEBUG: Ponto de verificação

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Cuiaba"
USE_I18N = True
USE_TZ = True
print("DEBUG: Configurações de internacionalização e fuso horário carregadas.") # DEBUG: Ponto de verificação

# Static files
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
print("DEBUG: Configurações de arquivos estáticos carregadas.") # DEBUG: Ponto de verificação

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuração CORS extra (fallback para dev)
if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == [""]:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://172.16.7.154:3000",
        "https://encantamais-frontend.vercel.app",
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_ALL_ORIGINS = False
print("DEBUG: Configurações CORS adicionais carregadas." ) # DEBUG: Ponto de verificação

# Usuário customizado
AUTH_USER_MODEL = "core.Usuario"
print("DEBUG: AUTH_USER_MODEL carregado.") # DEBUG: Ponto de verificação

# Configuração de Logging (Adicionada para depuração)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
print("DEBUG: Configuração de LOGGING adicionada e carregada.") # DEBUG: Ponto de verificação
