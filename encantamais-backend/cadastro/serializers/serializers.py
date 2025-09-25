from rest_framework import serializers
from cadastro.models import  Produto, FormaPagamento, ListaItem, FamiliaProduto
from django.conf import settings


class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = ['id_forma_pagamento', 'descricao', 'prazo_vencimento', 'tipo']



class FamiliaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamiliaProduto
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):

    imagem_url = serializers.SerializerMethodField()
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'tipo', 'preco', 'familia', 'imagem', 'imagem_url']

    def get_imagem_url(self, obj):
        request = self.context.get("request")
        if obj.imagem:
            return request.build_absolute_uri(obj.imagem.url)
        return request.build_absolute_uri(f"{settings.MEDIA_URL}produtos/default.jpg")  # URL absoluta da imagem padrão

class ListaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaItem
        fields = ["id", "descricao", "valor", "ordem", "lista_id"]
