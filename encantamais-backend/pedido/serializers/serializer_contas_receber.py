from rest_framework import serializers
from ..models.model_contas_receber import TituloReceber, TituloMovimento, TituloHistorico

class TituloHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TituloHistorico
        fields = '__all__'

class TituloMovimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TituloMovimento
        fields = '__all__'

class TituloReceberSerializer(serializers.ModelSerializer):
    movimentos = TituloMovimentoSerializer(many=True, read_only=True)
    historico = TituloHistoricoSerializer(many=True, read_only=True)

    class Meta:
        model = TituloReceber
        fields = '__all__'
