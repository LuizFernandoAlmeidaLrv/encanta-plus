from rest_framework import viewsets
from core.models import Cliente
from core.serializers.cliente import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('data_cadastro')
    serializer_class = ClienteSerializer
