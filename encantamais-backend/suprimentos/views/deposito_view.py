# suprimentos/views/deposito_view.py

from rest_framework import viewsets
from suprimentos.models.deposito import Deposito
from suprimentos.serializers.deposito_serializer import DepositoSerializer

class DepositoViewSet(viewsets.ModelViewSet):
    queryset = Deposito.objects.all()
    serializer_class = DepositoSerializer
