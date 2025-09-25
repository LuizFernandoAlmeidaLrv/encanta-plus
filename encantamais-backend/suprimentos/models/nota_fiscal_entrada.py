# suprimentos/models/nota_fiscal_entrada.py

from django.db import models
from core.models.fornecedor import Fornecedor

class NotaFiscalEntrada(models.Model):
    SITUACAO_CHOICES = [
        ('1', 'Digitada'),
        ('2', 'Fechada'),
        ('3', 'Cancelada'),
    ]

    numero = models.CharField(max_length=10)
    serie = models.CharField(max_length=5)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    data_emissao = models.DateField()
    data_entrada = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    observacao = models.TextField(blank=True)
    
    situacao = models.CharField(
        max_length=1,
        choices=SITUACAO_CHOICES,
        default='1'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('numero', 'serie', 'fornecedor')
        ordering = ['-numero']

    def __str__(self):
        return f"NF {self.numero}/{self.serie}"
