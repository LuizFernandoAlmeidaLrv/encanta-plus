from rest_framework import viewsets
from produtos.models.categoria import Categoria
from produtos.serializers.categoria_serializer import CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('nome')
    serializer_class = CategoriaSerializer
