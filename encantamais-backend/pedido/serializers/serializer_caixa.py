from rest_framework import serializers
from ..models.model_caixa import Caixa

class CaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = '__all__'
