"""
WSGI config for Encantamais project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EncantaMais.settings')

print("DEBUG: EncantaMais/wsgi.py está sendo carregado. Tentando obter aplicação WSGI...") # ADICIONE ESTA LINHA
application = get_wsgi_application()
print("DEBUG: Aplicação WSGI obtida com sucesso.") # ADICIONE ESTA LINHA
