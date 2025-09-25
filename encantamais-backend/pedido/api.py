from rest_framework import viewsets
from pedido.models import Pedido, PedidoItem, PedidoItemComposicao
from cadastro.models import Cliente, Produto, FormaPagamento, Cardapio
from pedido.serializers.serializer_pedido import (
    PedidoSerializer,
    PedidoItemComposicaoSerializer
)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

