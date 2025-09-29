from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import logging
from django.core.exceptions import ImproperlyConfigured

# Carrega .env da raiz do projeto (onde está manage.py)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Configurações de Segurança
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")

# Verificação explícita da SECRET_KEY
if not SECRET_KEY:
    print("DEBUG: SECRET_KEY está vazia ou não foi definida corretamente!")
    raise ImproperlyConfigured("A SECRET_KEY não pode ser vazia. Verifique as variáveis de ambiente do Render.")
else:
    print(f"DEBUG: SECRET_KEY lida com sucesso (tamanho: {len(SECRET_KEY)} caracteres).")

DEBUG = os.getenv("DJANGO_DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

print("DEBUG: settings.py está sendo carregado...")

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
    print("DEBUG: Configuração de banco de dados do Render (Postgres) carregada.")
else:
    # Local → SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("DEBUG: Configuração de banco de dados local (SQLite) carregada.")


# =========================
# Configurações de CORS e Media
# =========================
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

print("DEBUG: Configurações de CORS e Media carregadas.")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    "core",
    "produtos",
    "preco",
    "suprimentos",
    "vendas",
    "financeiro",
]
print("DEBUG: INSTALLED_APPS carregado.")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
print("DEBUG: MIDDLEWARE carregado.")

ROOT_URLCONF = 'EncantaMais.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
print("DEBUG: TEMPLATES carregado.")

WSGI_APPLICATION = 'EncantaMais.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
print("DEBUG: AUTH_PASSWORD_VALIDATORS carregado." )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
print("DEBUG: REST_FRAMEWORK carregado.")

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

print("DEBUG: Configurações de internacionalização e fuso horário carregadas." )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles' )

print("DEBUG: Configurações de arquivos estáticos carregadas.")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_ALL_ORIGINS = False

print("DEBUG: Configurações CORS adicionais carregadas." )

# Custom User Model
AUTH_USER_MODEL = 'usuarios.CustomUser'
print("DEBUG: AUTH_USER_MODEL carregado.")

# Configuração de Logging para depuração
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
print("DEBUG: Configuração de LOGGING adicionada e carregada.")
