# suprimentos/serializers/estoque_serializer.py

from rest_framework import serializers
from suprimentos.models.estoque import Estoque

class EstoqueSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    deposito_nome = serializers.CharField(source='deposito.nome', read_only=True)

    class Meta:
        model = Estoque
        fields = ['id', 'produto', 'produto_nome', 'deposito', 'deposito_nome', 'saldo', 'atualizado_em']
