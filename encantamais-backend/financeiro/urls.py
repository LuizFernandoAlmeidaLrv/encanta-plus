from django.urls import path, include
from rest_framework.routers import DefaultRouter
from financeiro.views.views_titulo_receber import TituloReceberViewSet
from financeiro.views.view_caixa import CaixaViewSet, CaixaMovimentoViewSet, BaixarTitulosAPIView

router = DefaultRouter()
router.register(r'titulos', TituloReceberViewSet)
router.register(r'caixas', CaixaViewSet)
router.register(r'caixa_movimentos', CaixaMovimentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('baixar_titulos/', BaixarTitulosAPIView.as_view(), name='baixar_titulos'),
]
