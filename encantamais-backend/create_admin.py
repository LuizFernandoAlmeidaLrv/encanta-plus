import os
import django

# Aponta para o settings do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EncantaMais.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do superusuário
USERNAME = "admin"
EMAIL = "admin@encanta.com"
PASSWORD = "SenhaForte123"  # troque para algo seguro

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe.")
