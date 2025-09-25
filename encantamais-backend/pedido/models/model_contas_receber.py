from django.db import models
from django.contrib.auth.models import User
from pedido.models.model_pedido import Pedido  # Supondo que você já tenha o modelo de Pedido
from cadastro.models import Cliente


class TituloReceber(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="titulos")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ABERTO', 'Aberto'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado')
    ], default='ABERTO')
    forma_pagamento = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    usuario_criacao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="titulos_criados")
    usuario_baixa = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="titulos_baixados")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Título #{self.id} - {self.cliente.nome} - R$ {self.valor_total}"

class TituloMovimento(models.Model):
    titulo = models.ForeignKey(TituloReceber, on_delete=models.CASCADE, related_name="movimentos")
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20)
    observacao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Movimento Título #{self.titulo.id} - R$ {self.valor}"

class TituloHistorico(models.Model):
    titulo = models.ForeignKey(TituloReceber, on_delete=models.CASCADE, related_name="historico")
    data = models.DateTimeField(auto_now_add=True)
    status_anterior = models.CharField(max_length=20)
    status_novo = models.CharField(max_length=20)
    observacao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Histórico Título #{self.titulo.id} - {self.status_anterior} → {self.status_novo}"
