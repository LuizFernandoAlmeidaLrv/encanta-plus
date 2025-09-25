from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FamiliaProduto, Produto, FormaPagamento, Lista, ListaItem



@admin.register(FamiliaProduto)
class FamiliaProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Exibe o ID e o nome da família na lista
    search_fields = ('nome',)  # Permite buscar pelo nome da família
    ordering = ('nome',)  # Ordena por nome

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao','preco', 'familia', 'imagem')
    list_filter = ('familia',)  # Filtro por família no admin
    search_fields = ('nome','familia__nome')  # Busca pelo nome do produto e nome da família
    ordering = ('familia', 'nome')  # Ordena por família e nome do produto


 
@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('id_forma_pagamento', 'descricao', 'prazo_vencimento', 'tipo')
    ordering = ('id_forma_pagamento',)

@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'lista')  # Mostra esses campos na listagem
    search_fields = ('descricao', 'lista')  # Permite buscar por descrição e nome interno
    list_per_page = 20  # Paginação para evitar sobrecarga na interface

@admin.register(ListaItem)
class ListaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'lista', 'descricao', 'ordem', 'valor')  # Campos exibidos
    list_filter = ('lista',)  # Filtro lateral para facilitar busca por categorias
    search_fields = ('descricao', 'valor')  # Permite busca por descrição e valor
    list_editable = ('ordem', 'valor')  # Permite editar diretamente na listagem
    list_per_page = 20  # Paginação

    # Exibir os itens agrupados pela lista no Django Admin
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('lista').order_by('lista', 'ordem')

