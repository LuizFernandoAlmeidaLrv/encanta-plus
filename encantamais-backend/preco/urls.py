from django.urls import path, include
from rest_framework.routers import DefaultRouter
from preco.views.view_ultimo_custo import UltimoCustoAPIView
from preco.views.view_preco import (
    TabelaPrecoViewSet,
    FormacaoPrecoViewSet,
    FormacaoPrecoByProdutoAPIView,
    TabelaPrecoProdutoViewSet,
    HistoricoFormacaoPrecoViewSet,
)

router = DefaultRouter()
router.register(r'tabela_preco', TabelaPrecoViewSet)
router.register(r'tabela_preco_produto', TabelaPrecoProdutoViewSet)
router.register(r'historico_formacao_preco', HistoricoFormacaoPrecoViewSet)
router.register(r'formacao_preco', FormacaoPrecoViewSet, basename='formacaopreco')  # <-- Adicionado aqui

urlpatterns = [
    path('', include(router.urls)),
    path("formacao_preco_por_produto/<str:produto_id>/", FormacaoPrecoByProdutoAPIView.as_view()),  # <-- Sobrescreve o GET com lógica extra
    path("ultimo_custo/<str:produto_id>/", UltimoCustoAPIView.as_view()),  # ✅ Adicione assim
]
