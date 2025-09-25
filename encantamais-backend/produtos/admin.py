from django.contrib import admin

from produtos.models.categoria import Categoria
from produtos.models.produto import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'categoria', 'tamanho', 'cor', 'custo_ultimo',  'codigo_agrupamento')
    list_filter = ('categoria', 'cor', 'tamanho')
    search_fields = ('nome', 'codigo', 'codigo_agrupamento')

admin.site.register(Categoria)
