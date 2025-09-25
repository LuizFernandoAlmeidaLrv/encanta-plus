from rest_framework import serializers
from produtos.models.produtocusto import ProdutoCusto

class ProdutoCustoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_codigo = serializers.CharField(source='produto.codigo', read_only=True)
    usuario_nome = serializers.CharField(source='usuario_gerador.username', read_only=True)

    class Meta:
        model = ProdutoCusto
        fields = '__all__'  # já inclui os campos do model + os 3 acima
        extra_kwargs = {
            'sequencia': {'read_only': True},
            'usuario_gerador': {'required': False}
        }
