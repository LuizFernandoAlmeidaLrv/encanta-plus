from rest_framework import serializers
from financeiro.models.models_titulo_receber import TituloReceber
from financeiro.models.models_titulo_movimento import TituloMovimento
from core.serializers.forma_pagamento import FormaPagamentoSerializer
from core.serializers.cliente import ClienteSerializer
from core.models import FormaPagamento, Cliente
from vendas.models import Venda
from vendas.serializers.serializers_venda import VendaSerializer


class TituloMovimentoSerializer(serializers.ModelSerializer):
    forma_pagamento = FormaPagamentoSerializer(read_only=True)
    forma_pagamento_id = serializers.PrimaryKeyRelatedField(
        queryset=FormaPagamento.objects.all(),
        source='forma_pagamento',
        write_only=True
    )

   
    class Meta:
        model = TituloMovimento
        fields = [
            "id", 
            "titulo_receber",
            "tipo",
            "data_movimento",
            "valor",
            "forma_pagamento",
            "forma_pagamento_id",
            "situacao",
            "observacao",
            ]
        read_only_fields = ('id', 'data_movimento')

class TituloReceberSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(
    queryset=Cliente.objects.all(),
    write_only=True
)

    venda = serializers.PrimaryKeyRelatedField(
        queryset=Venda.objects.all(), 
        write_only=True
    )
    movimentos = TituloMovimentoSerializer(many=True, read_only=True)
    data_venda = serializers.SerializerMethodField()
    data_vencimento = serializers.DateField()
    data_recebimento = serializers.SerializerMethodField()

    def get_data_venda(self, obj):
        return obj.venda.data_venda.date() if obj.venda and obj.venda.data_venda else None

    def get_data_vencimento(self, obj):
        return obj.data_vencimento if obj.data_vencimento else None

    def get_data_recebimento(self, obj):
        return obj.data_recebimento if obj.data_recebimento else None
    forma_pagamento = FormaPagamentoSerializer(read_only=True)
    forma_pagamento_id = serializers.PrimaryKeyRelatedField(
        queryset=FormaPagamento.objects.all(),
        source='forma_pagamento',
        write_only=True
    )

    class Meta:
        model = TituloReceber
        fields = [
            "id",
            "venda",
            "cliente",
            "data_venda",
            "data_vencimento",
            "data_recebimento",
            "valor",
            "valor_aberto",
            "situacao",
            "forma_pagamento",
            "forma_pagamento_id",
            "movimentos",
        ]



