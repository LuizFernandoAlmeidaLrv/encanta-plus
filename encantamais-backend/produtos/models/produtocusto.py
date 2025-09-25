from django.db import models
from django.conf import settings
from produtos.models.produto import Produto  # ajuste conforme seu app
from django.conf import settings



class ProdutoCusto(models.Model):
    SIT_CUSTO_CHOICES = [
        ('N', 'Não Processado'),
        ('C', 'Cancelado'),
        ('P', 'Processado'),
    ]
    ATUALIZA_CUSTO_CHOICES = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]
    TIPO_CUSTO_CHOICES = [
        ('M', 'Manual'),
        ('A', 'Automático'),
    ]
    # Deixa o Django criar o ID automaticamente
    # ou declare explicitamente:
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_custo = models.DateField()
    sequencia = models.IntegerField()
    valor_base = models.DecimalField(max_digits=13, decimal_places=4, null=True, blank=True)
    perc_frete = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_custo = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    custo_medio = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    tipo_custo = models.CharField(max_length=1, choices=TIPO_CUSTO_CHOICES, null=True, blank=True)
    cod_fornecedor = models.IntegerField(null=True, blank=True)
    numero_nota = models.IntegerField(null=True, blank=True)
    serie_nota = models.CharField(max_length=3, null=True, blank=True)
    seq_item = models.IntegerField(null=True, blank=True)
    situacao = models.CharField(max_length=1, choices=SIT_CUSTO_CHOICES, default='N')
    usuario_gerador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_geracao = models.DateField(null=True, blank=True)
    hora_geracao = models.IntegerField(null=True, blank=True)
    atualiza_custo_preco = models.CharField(max_length=1, choices=ATUALIZA_CUSTO_CHOICES, default='S')
    usuario_alteracao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='custos_alterados')
    data_alteracao = models.DateField(null=True, blank=True)
    hora_alteracao = models.IntegerField(null=True, blank=True)
    observacao = models.CharField(max_length=100, null=True, blank=True)
    valor_frete = models.DecimalField(max_digits=13, decimal_places=4, null=True, blank=True)

    class Meta:
        unique_together = ('produto', 'data_custo', 'sequencia')
        ordering = ['-data_custo']
