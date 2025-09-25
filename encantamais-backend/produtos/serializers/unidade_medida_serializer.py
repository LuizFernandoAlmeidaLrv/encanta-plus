# produtos/serializers/unidade_medida_serializer.py

from rest_framework import serializers
from produtos.models.unidade_medida import UnidadeMedida

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ['codigo', 'nome']
