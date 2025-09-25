# suprimentos/serializers/estoque_movimento_serializer.py

from rest_framework import serializers
from suprimentos.models.estoque_movimento import EstoqueMovimento

class EstoqueMovimentoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    deposito_nome = serializers.CharField(source='deposito.nome', read_only=True)

    class Meta:
        model = EstoqueMovimento
        fields = [
            'id', 'data', 'produto', 'produto_nome', 'deposito', 'deposito_nome',
            'tipo', 'quantidade', 'quantidade_estoque', 'quantidade_anterior',
            'chave_origem', 'historico'
        ]
