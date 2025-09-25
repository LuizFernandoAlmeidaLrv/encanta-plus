# estoque/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from suprimentos.views.nota_fiscal_entrada_view import NotaFiscalEntradaViewSet
from suprimentos.views.deposito_view import DepositoViewSet
from suprimentos.views.nota_fiscal_entrada_view import NotaFiscalEntradaViewSet
from suprimentos.views.estoque_view import EstoqueViewSet
from suprimentos.views.estoque_movimento_view import EstoqueMovimentoViewSet

router = DefaultRouter()
router.register(r'depositos', DepositoViewSet, basename='deposito')
router.register(r'estoques', EstoqueViewSet, basename='estoque')
router.register(r'movimentos-estoque', EstoqueMovimentoViewSet, basename='estoquemovimento')
router.register(r'notas-entrada', NotaFiscalEntradaViewSet, basename='notaentrada')

urlpatterns = [
    path('', include(router.urls)),
]
