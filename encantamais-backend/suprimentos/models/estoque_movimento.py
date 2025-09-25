# suprimentos/models/estoque_movimento.py

from django.db import models
from core.models import Fornecedor, Cliente  # ajuste o import se o app for diferente
from produtos.models.produto import Produto
from suprimentos.models.deposito import Deposito
from vendas.models.models_venda import Venda, VendaItem  # ou o app correto


class EstoqueMovimento(models.Model):
    TIPO_MOVIMENTO = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        
    ]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=2, choices=TIPO_MOVIMENTO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    quantidade_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_estoque = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True)
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT, null=True, blank=True)
    venda_item = models.ForeignKey(VendaItem, on_delete=models.PROTECT, null=True, blank=True)

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, blank=True)
    numero_nota = models.CharField(max_length=20, blank=True, null=True)
    serie_nota = models.CharField(max_length=10, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.tipo == 'E':
            return f"{self.produto.nome} - Entrada {self.quantidade} (NF {self.numero_nota})"
        else:
            return f"{self.produto.nome} - Saída {self.quantidade} (Venda {self.venda_id})"
