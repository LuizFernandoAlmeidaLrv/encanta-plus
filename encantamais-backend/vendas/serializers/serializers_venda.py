# vendas/serializers.py
from rest_framework import serializers
from vendas.models.models_venda import Venda, VendaItem
from vendas.models.models_venda_parcela import VendaParcela
from core.serializers.cliente import ClienteSerializer
from core.serializers.forma_pagamento import FormaPagamentoSerializer
from core.models import Cliente, FormaPagamento, Usuario



class VendaItemSerializer(serializers.ModelSerializer):
    nome_produto = serializers.SerializerMethodField()
    
    class Meta:
        model = VendaItem
        fields = [
            'id',
            'produto',
            'quantidade',
            'valor_unitario',
            'valor_total',
            'venda',
            'nome_produto',
            'deposito',
        ]

    def get_nome_produto(self, obj):
        if obj.produto:
            return f"{obj.produto.codigo} - {obj.produto.nome}"
        return ""

class VendaParcelaSerializer(serializers.ModelSerializer):
    forma_pagamento = FormaPagamentoSerializer(read_only=True)
    forma_pagamento_id = serializers.PrimaryKeyRelatedField(
    queryset=FormaPagamento.objects.all(),
    source='forma_pagamento',
    write_only=True
    )
    class Meta:
        model = VendaParcela
        fields = [
            'id',
            'numero_parcela',
            'quantidade_parcelas',
            'data_vencimento',
            'valor_parcela',
            'situacao',
            'venda',
            'forma_pagamento',
            'forma_pagamento_id',
        ]

class VendaSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(
    queryset=Usuario.objects.all(),
    source='usuario',  # importante: mapeia pro campo do model
    write_only=True
)
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), source="cliente", write_only=True)
    itens = VendaItemSerializer(many=True, read_only=True)
    parcelas_venda = VendaParcelaSerializer(many=True, read_only=True)
    forma_pagamento = FormaPagamentoSerializer(read_only=True)
    forma_pagamento_id = serializers.PrimaryKeyRelatedField(
    queryset=FormaPagamento.objects.all(),
    source='forma_pagamento',
    write_only=True
)
    class Meta:
        model = Venda
        fields = [
            'id', 
            'cliente', 
            'data_venda', 
            'data_liberacao',
            'valor_total', 
            'situacao',  # Pendente, Fechada, etc.
            'tipo', # Avista, Prazo
            'itens', 
            'parcelas_venda',
            'cliente_id',
            'forma_pagamento',
            'forma_pagamento_id',
            'usuario_id',

        ]
    def create(self, validated_data):
        # Se não vier usuario, pega do request
        if 'usuario' not in validated_data:
            validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
    def to_internal_value(self, data):
        print("\n--- Dados crus recebidos no Serializer ---")
        print(data)
        print("------------------------------------------\n")
        return super().to_internal_value(data)