# suprimentos/views/estoque_movimento_view.py

from rest_framework import viewsets
from suprimentos.models.estoque_movimento import EstoqueMovimento
from suprimentos.serializers.estoque_movimento_serializer import EstoqueMovimentoSerializer

class EstoqueMovimentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstoqueMovimento.objects.all()
    serializer_class = EstoqueMovimentoSerializer
