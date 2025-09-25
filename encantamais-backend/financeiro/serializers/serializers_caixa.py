from rest_framework import serializers
from financeiro.models.models_caixa import Caixa, CaixaMovimento

class CaixaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario.nome_completo", read_only=True)

    class Meta:
        model = Caixa
        fields = '__all__'


class CaixaMovimentoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario.nome_completo", read_only=True)
    forma_pagamento_nome = serializers.CharField(source="forma_pagamento.descricao", read_only=True)

    class Meta:
        model = CaixaMovimento
        fields = '__all__'
