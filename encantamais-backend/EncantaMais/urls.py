from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Função simples para testar
def home(request):
    return HttpResponse("Bem-vindo ao EncantaMais!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('produtos.urls')),  # Inclui as rotas do cadastro
    path('api/', include('suprimentos.urls')),
    path('api/', include('preco.urls')),
    path('api/', include('vendas.urls')),
    path('api/', include('financeiro.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home),  # ← Adicione esta linha para a raiz
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    