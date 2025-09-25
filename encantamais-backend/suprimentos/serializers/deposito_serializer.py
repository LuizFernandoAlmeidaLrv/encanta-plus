# suprimentos/serializers/deposito_serializer.py

from rest_framework import serializers
from suprimentos.models.deposito import Deposito

class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['codigo', 'nome', 'descricao']
