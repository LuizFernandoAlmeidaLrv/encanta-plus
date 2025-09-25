# produtos/apps.py

from django.apps import AppConfig

class ProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produtos'

    def ready(self):
        import produtos.signals  # 👈 Importa e ativa o sinal
