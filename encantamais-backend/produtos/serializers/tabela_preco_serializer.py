
from rest_framework import serializers
from produtos.models.tabela_preco import TabelaPreco
from produtos.models.tabela_preco_produto import TabelaPrecoProduto



class TabelaPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPreco
        fields = '__all__'

class TabelaPrecoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPrecoProduto
        fields = '__all__'
