from django.db import models
from financeiro.models.models_titulo_receber import TituloReceber
from core.models import FormaPagamento

TIPOS_MOVIMENTO = (
    ('E', 'Entrada'),  # Lançamento inicial do título
    ('B', 'Baixa'),   # Pagamento ou baixa parcial do título
)

SITUACAO_MOVIMENTO = (
    ('A', 'Ativo'),
    ('I', 'Inativo'), 
)



class TituloMovimento(models.Model):
    titulo_receber = models.ForeignKey(TituloReceber, on_delete=models.CASCADE, related_name='movimentos')
    tipo = models.CharField(max_length=1, choices=TIPOS_MOVIMENTO)
    data_movimento = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        related_name='movimentos_titulo'
    )
    observacao = models.TextField(blank=True, null=True)
    situacao = models.CharField(max_length=1, choices=SITUACAO_MOVIMENTO, default='A')

    def __str__(self):
        return f'Movimento #{self.id} - Título #{self.titulo_receber.id} - {self.get_tipo_display()} - {self.valor}'
