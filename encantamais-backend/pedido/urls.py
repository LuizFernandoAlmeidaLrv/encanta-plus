from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pedido.views.view_pedido import (PedidoViewSet, ComposicaoViewSet,)
from pedido.views.view_pedido import (FormaPagamentoViewSet, ListaItemViewSet,)
from cadastro.views import FamiliaProdutoViewSet
from .views.view_contas_receber import (
    TituloReceberViewSet,
    TituloMovimentoViewSet,
    TituloHistoricoViewSet,
)
from .views.view_caixa import CaixaStatusViewSet # ✅ Correta importação das views de caixa

# Inicializa o router para registrar os viewsets
router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'formaspagamento', FormaPagamentoViewSet)
router.register(r'composicao', ComposicaoViewSet, basename='composicao')
router.register(r'listaitem', ListaItemViewSet)
router.register(r'titulos-receber', TituloReceberViewSet, basename='titulos-receber')
router.register(r'titulos-movimentos', TituloMovimentoViewSet, basename='titulos-movimentos')
router.register(r'titulos-historico', TituloHistoricoViewSet, basename='titulos-historico')
router.register(r'caixa', CaixaStatusViewSet, basename='caixa')

# 🔥 Definição correta do urlpatterns (sem sobrescrever!)
urlpatterns = [
    path('', include(router.urls)),  # Inclui as URLs dos ViewSets (DRF)    
    # URLs do caixa (verificação e abertura)
]
