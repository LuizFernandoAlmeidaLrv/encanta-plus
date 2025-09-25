from django.urls import include, path
from rest_framework.routers import DefaultRouter
from produtos.views.categoria_view import CategoriaViewSet
from produtos.views.produto_view import ProdutoViewSet, buscar_produto_por_codigo
from produtos.views.unidade_medida_view import UnidadeMedidaViewSet
from produtos.views.produto_custo_view import ProdutoCustoViewSet


router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet)
router.register(r'unidades-medida', UnidadeMedidaViewSet, basename='unidade-medida')
router.register(r'produto_custos', ProdutoCustoViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('produtos/buscar_por_codigo/<str:codigo>/', buscar_produto_por_codigo),
 
]
