from django.db import models
from django.contrib.auth.models import User
from .model_caixa import Caixa
from .model_caixa_despesa import CaixaTipoDespesa
class CaixaMovimento(models.Model):
    TIPO_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("SAIDA", "Saída"),
        ("TRANSFERENCIA", "Transferência"),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimento = models.DateTimeField(auto_now_add=True)
    historico = models.TextField()

    titulo_movimento = models.ForeignKey('TituloReceberMovimento', on_delete=models.SET_NULL, null=True, blank=True)
    transferencia = models.ForeignKey('CaixaTransferencia', on_delete=models.SET_NULL, null=True, blank=True)
    despesa = models.ForeignKey('CaixaDespesa', on_delete=models.SET_NULL, null=True, blank=True)
    vale = models.ForeignKey('CaixaVale', on_delete=models.SET_NULL, null=True, blank=True)
    
    caixa = models.ForeignKey('Caixa', on_delete=models.CASCADE, related_name="movimentos")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    situacao = models.CharField(max_length=1, choices=[("A", "Ativo"), ("I", "Inativo")], default="A")

    def __str__(self):
        return f"{self.tipo} - R$ {self.valor} - {self.data_movimento.strftime('%d/%m/%Y')}"
