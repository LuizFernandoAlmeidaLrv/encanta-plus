# produtos/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from produtos.models.produto import Produto
from suprimentos.models.estoque import Estoque
from suprimentos.models.deposito import Deposito

@receiver(post_save, sender=Produto)
def criar_estoque_padrao(sender, instance, created, **kwargs):
    if created:
        try:
            deposito_padrao = Deposito.objects.get(codigo='E001')
            Estoque.objects.get_or_create(
                produto=instance,
                deposito=deposito_padrao,
                defaults={'saldo': 0}
            )
        except Deposito.DoesNotExist:
            # Se quiser pode logar um warning aqui
            print("Depósito E001 não encontrado. Não foi possível criar o estoque.")
