from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import FormaPagamento
from core.serializers.forma_pagamento import FormaPagamentoSerializer, FormaPagamentoSelectSerializer



class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer

    @action(detail=False, methods=["get"])
    def select(self, request):
        queryset = self.get_queryset().filter(situacao="A")
        serializer = FormaPagamentoSelectSerializer(queryset, many=True)
        return Response(serializer.data)