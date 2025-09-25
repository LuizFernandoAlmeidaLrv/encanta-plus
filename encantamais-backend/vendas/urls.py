from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vendas.views.views_venda import VendaViewSet, VendaItemViewSet, VendaParcelaViewSet

router = DefaultRouter()

router.register(r'vendas', VendaViewSet)
router.register(r'venda_itens', VendaItemViewSet)
router.register(r'venda_parcelas', VendaParcelaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
