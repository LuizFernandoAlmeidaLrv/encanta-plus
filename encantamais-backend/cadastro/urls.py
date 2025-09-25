from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from cadastro.views.views import FamiliaProdutoViewSet, ProdutoViewSet
from django.conf.urls.static import static


# Inicializa o router para registrar os viewsets
router = DefaultRouter()

router.register(r'familias', FamiliaProdutoViewSet, basename='familia')
router.register(r'produtos', ProdutoViewSet)


# As URLs serão registradas pelo router
urlpatterns = [
    path('', include(router.urls)),  # Inclui as URLs do router
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)