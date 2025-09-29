from django.db import models
from produtos.models.produto import Produto  # ajuste conforme seu app
from django.conf import settings

class FormacaoPreco(models.Model):
    produto = models.OneToOneField(  # Chave primária
        Produto, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    custo_base = models.DecimalField(  # valor manual, usado como base
        max_digits=10, decimal_places=4, default=0
    )
    valor_custo = models.DecimalField(  # último custo registrado
        max_digits=15, decimal_places=4, null=True, blank=True
    )
    custo_com_frete = models.DecimalField(  # opcional, para custo total
        max_digits=10, decimal_places=4, default=0
    )
    margem_lucro = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    margem_custo_fixo = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    valor_venda_sugerido = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Formação Preço - {self.produto}'



class FormacaoPrecoHistorico(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    custo_base = models.DecimalField(max_digits=10, decimal_places=4)
    custo_com_frete = models.DecimalField(max_digits=10, decimal_places=4)
    margem_lucro = models.DecimalField(max_digits=5, decimal_places=2)
    margem_custo_fixo = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_venda_sugerido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data_alteracao']