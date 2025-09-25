from rest_framework import serializers
from django.db import models
from produtos.models.produto import Produto
from suprimentos.models.estoque import Estoque
from datetime import date
from preco.models.tabela_preco_produto import TabelaPrecoProduto

class ProdutoSerializer(serializers.ModelSerializer):
    saldo = serializers.SerializerMethodField()
    deposito = serializers.SerializerMethodField()
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.nome', read_only=True)
    imagem = serializers.ImageField(required=False, allow_null=True, use_url=True)
    codigo = serializers.CharField(required=False, allow_blank=True)
    preco_normal = serializers.SerializerMethodField()
    preco_promocional = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'categoria', 'categoria_nome',
            'fornecedor', 'fornecedor_nome', 'cor', 'tamanho',
            'codigo_agrupamento', 'imagem', 'criado_em', 'atualizado_em',
            'preco_normal', 'preco_promocional', 'saldo', 'deposito'
        ]

    def get_precos_validos(self, produto):
        # Usa o atributo pré-carregado no queryset para evitar consulta extra
        return getattr(produto, 'precos_validos', [])

    def get_preco_normal(self, produto):
        precos = self.get_precos_validos(produto)
        preco_normal = next(
            (p for p in precos if p.tabela_preco.nome == 'Normal'),
            None
        )
        if preco_normal:
            return preco_normal.preco_venda
        return None

    def get_preco_promocional(self, produto):
        precos = self.get_precos_validos(produto)
        precos_promo = [p for p in precos if p.tabela_preco.nome != 'Normal']
        if precos_promo:
            # Retorna o menor preço promocional
            menor_promo = min(precos_promo, key=lambda p: p.preco_venda)
            return menor_promo.preco_venda
        return None
    
    def get_saldo(self, obj):
        # Pega o saldo do estoque principal ou primeiro depósito
        estoque = Estoque.objects.filter(produto=obj).first()
        return estoque.saldo if estoque else 0

    def get_deposito(self, obj):
        estoque = Estoque.objects.filter(produto=obj).first()
        return estoque.deposito.codigo if estoque else "E001"
