from rest_framework import viewsets
from core.models import Fornecedor
from core.serializers.fornecedor import FornecedorSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all().order_by('data_cadastro')
    serializer_class = FornecedorSerializer
