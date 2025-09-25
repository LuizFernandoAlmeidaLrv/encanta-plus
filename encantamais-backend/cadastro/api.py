from rest_framework import viewsets
from cadastro.models import Ingrediente, CardapioIngredientes, Cliente, Produto, FormaPagamento, Cardapio
from cadastro.serializers import IngredienteSerializer, CardapioIngredientesSerializer, ClienteSerializer, ProdutoSerializer, FormaPagamentoSerializer, CardapioSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class CardapioIngredientesViewSet(viewsets.ModelViewSet):
    queryset = CardapioIngredientes.objects.all()
    serializer_class = CardapioIngredientesSerializer

class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer

class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.all()
    serializer_class = CardapioSerializer