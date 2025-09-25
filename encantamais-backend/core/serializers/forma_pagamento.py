from rest_framework import serializers
from core.models import FormaPagamento

class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = '__all__'

class FormaPagamentoSelectSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="id")
    label = serializers.CharField(source="descricao")

    class Meta:
        model = FormaPagamento
        fields = ["value", "label"]