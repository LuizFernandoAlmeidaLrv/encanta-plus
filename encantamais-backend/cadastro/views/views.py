from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from cadastro.models import FamiliaProduto, Produto, FormaPagamento, Lista, ListaItem


from cadastro.serializers.serializers import FormaPagamentoSerializer, FamiliaProdutoSerializer, ProdutoSerializer

class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer

 
class FamiliaProdutoViewSet(viewsets.ModelViewSet):
    queryset = FamiliaProduto.objects.all().order_by('nome')
    serializer_class = FamiliaProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = Produto.objects.all()
        familia_id = self.request.query_params.get("familiaid")
        if familia_id:
            queryset = queryset.filter(familia_id=familia_id)
        return queryset

