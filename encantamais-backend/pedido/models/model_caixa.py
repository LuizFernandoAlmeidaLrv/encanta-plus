from django.db import models
from django.contrib.auth.models import User

class Caixa(models.Model):
    SITUACAO_CHOICES = [
        ("A", "Aberto"),
        ("F", "Fechado"),
    ]

    data_caixa = models.DateField(primary_key=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    data_proximo_caixa = models.DateField(null=True, blank=True)

    moeda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bancos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pix = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    cartoes = models.IntegerField(default=0)
    cartoes_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cartoes_credito_operacao_0 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cartoes_credito_operacao_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cartoes_credito_operacao_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    adiantamentos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    despesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_despesas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    receitas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_receitas = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    situacao = models.CharField(max_length=1, choices=SITUACAO_CHOICES, default="A")

    usuarios_abertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='caixas_abertos')
    usuario_fechamento = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='caixas_fechados')

    def __str__(self):
        return f"Caixa {self.data_caixa}"
