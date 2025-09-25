# produtos/views/unidade_medida_view.py

from rest_framework import viewsets
from produtos.models.unidade_medida import UnidadeMedida
from produtos.serializers.unidade_medida_serializer import UnidadeMedidaSerializer

class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    lookup_field = 'codigo'  # <- Importante: usar 'codigo' nas URLs
