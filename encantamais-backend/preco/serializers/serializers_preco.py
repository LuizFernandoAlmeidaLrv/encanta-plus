from rest_framework import serializers
from preco.models import (
    TabelaPreco,
    FormacaoPreco,
    TabelaPrecoProduto,
    FormacaoPrecoHistorico,
)

class TabelaPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPreco
        fields = '__all__'



class FormacaoPrecoSerializer(serializers.ModelSerializer):
    codigo_produto = serializers.CharField(source='produto.codigo', read_only=True)
    nome_produto = serializers.CharField(source='produto.nome', read_only=True)  # <-- Adicionado

    class Meta:
        model = FormacaoPreco
        fields = '__all__'        


class TabelaPrecoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPrecoProduto
        fields = '__all__'

class HistoricoFormacaoPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormacaoPrecoHistorico
        fields = '__all__'
