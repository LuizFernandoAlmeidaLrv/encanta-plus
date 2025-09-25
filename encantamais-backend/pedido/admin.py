from django.contrib import admin
from pedido.models import Pedido, PedidoItem,PedidoItemComposicao


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1  # Permite adicionar novos itens ao criar um pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("numero_pedido", "cliente", "situacao_do_pedido", "valor_pedido", "data_inicio_pedido")
    search_fields = ("numero_pedido", "cliente__nome")
    list_filter = ("situacao_do_pedido", "data_inicio_pedido")
    inlines = [PedidoItemInline]

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade_pedida", "valor_total")
    search_fields = ("pedido__numero_pedido", "produto__nome")


@admin.register(PedidoItemComposicao)
class PedidoItemComposicaoAdmin(admin.ModelAdmin):
    list_display = ("pedido_item", "ingrediente", "quantidade", "observacao")  # 🔄 Troca item_cardapio por ingrediente
    list_filter = ("pedido_item__pedido", "ingrediente")  # 🔄 Troca item_cardapio por ingrediente
    search_fields = ("pedido_item__pedido__numero_pedido", "ingrediente__nome")  # 🔄 Troca item_cardapio por ingrediente
