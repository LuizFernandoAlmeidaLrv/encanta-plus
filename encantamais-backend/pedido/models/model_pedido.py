from django.db import models
from django.utils.timezone import now
from core.models import Cliente
from cadastro.models import Produto, FormaPagamento  # Importando produtos (Marmitas, Bebidas etc.)
from django.contrib.auth.models import User  # Usuário que gerou o pedido


tipo_pedido = models.IntegerField(choices=[(1, 'Entrega'), (2, 'Retirada'), (3, 'Consumo no local')], default=1)

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Pedido(models.Model):
    numero_pedido = models.AutoField(primary_key=True)

    TIPO_ENTREGA_CHOICES = [
        (1, 'Entrega'),
        (2, 'Retirada'),
        (3, 'Consumo no local'),
    ]
    forma_de_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, db_column='forma_de_pagamento_id') 
    tipo_entrega = models.IntegerField(choices=TIPO_ENTREGA_CHOICES)
    observacao_pedido = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  
    situacao_do_pedido = models.CharField(max_length=2)  

    quantidade = models.DecimalField(max_digits=14, decimal_places=5, default=0)  
    quantidade_aberta = models.DecimalField(max_digits=14, decimal_places=5, default=0)  
    valor_pedido = models.DecimalField(max_digits=15, decimal_places=2, default=0)


    # Datas e horários
    data_aprovacao_pedido = models.DateField(null=True, blank=True)
    hora_aprovacao_pedido = models.TimeField(null=True, blank=True)
    data_inicio_pedido = models.DateField(default=now)
    hora_inicio_pedido = models.TimeField(default=now)
    data_fim_pedido = models.DateField(null=True, blank=True)
    hora_fim_pedido = models.TimeField(null=True, blank=True)

    # Usuário que gerou o pedido
    usuario_gerador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_geracao = models.DateField(default=now)
    hora_geracao = models.TimeField(default=now)

    def calcular_total(self):
        return sum(item.valor_total for item in self.itens.all()) if self.pk and self.itens.exists() else 0

    def save(self, *args, **kwargs):
        # Se o pedido já foi salvo anteriormente, calcular os valores antes de salvar novamente
        if self.pk:
            self.valor_pedido = self.calcular_total()
            self.quantidade = sum(item.quantidade_pedida for item in self.itens.all()) if self.itens.exists() else 0

        super().save(*args, **kwargs)  # Salvar apenas uma vez

    def __str__(self):
        try:
            return f"Pedido #{self.numero_pedido} - Cliente: {self.cliente.nome if self.cliente else 'Sem Cliente'}"
        except:
            return f"Pedido #{self.numero_pedido} - Cliente: Erro ao carregar"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_pedida = models.DecimalField(max_digits=14, decimal_places=5, default=1)
    quantidade_aberta = models.DecimalField(max_digits=14, decimal_places=5, default=1)
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    observacao = models.TextField(blank=True, null=True)
    eh_marmita = models.BooleanField(default=False)  # Identifica se é uma marmita

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade_pedida * self.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade_pedida} un - Pedido {self.pedido.numero_pedido}"


class PedidoItemComposicao(models.Model):
    pedido_item = models.ForeignKey(PedidoItem, on_delete=models.CASCADE, related_name="composicoes", null=False)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=14, decimal_places=5)
    observacao = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Composição {self.ingrediente.nome} - Quantidade: {self.quantidade}"
    
class Composicao(models.Model):
    produto = models.ForeignKey(Produto, related_name="composicoes", on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)

