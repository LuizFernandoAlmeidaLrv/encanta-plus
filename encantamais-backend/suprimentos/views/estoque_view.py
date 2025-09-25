# suprimentos/views/estoque_view.py

from rest_framework import viewsets
from suprimentos.models.estoque import Estoque
from suprimentos.serializers.estoque_serializer import EstoqueSerializer

class EstoqueViewSet(viewsets.ReadOnlyModelViewSet):  # Apenas leitura
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
