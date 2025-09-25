# suprimentos/serializers/nota_fiscal_entrada_item_serializer.py

from rest_framework import serializers
from suprimentos.models.nota_item_entrada import NotaFiscalEntradaItem

class NotaFiscalEntradaItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = NotaFiscalEntradaItem
        fields = [
            'id', 'produto', 'produto_nome', 'quantidade', 'valor_unitario', 'valor_total',
            'percentual_frete', 'valor_frete_aplicado', 'custo_unitario_calculado',
            'aplicar_custo', 'deposito'
        ]
