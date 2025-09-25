from django.db import models
from django.contrib.auth.models import User
class CaixaTipoDespesa(models.Model):
    descricao = models.CharField(max_length=100)
    situacao = models.CharField(max_length=1, choices=[("A", "Ativo"), ("I", "Inativo")], default="A")

    def __str__(self):
        return self.descricao
class CaixaDespesa(models.Model):
    tipo_despesa = models.ForeignKey(CaixaTipoDespesa, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_despesa = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(help_text="Descrição ou observação da despesa")
    caixa = models.ForeignKey('Caixa', on_delete=models.CASCADE, related_name="despesas")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    situacao = models.CharField(max_length=1, choices=[("A", "Ativo"), ("I", "Inativo")], default="A")

    def __str__(self):
        return f"{self.tipo_despesa} - R$ {self.valor}"
