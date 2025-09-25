from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.fornecedor import FornecedorViewSet
from .views.cliente import ClienteViewSet
from .views.forma_pagamento import FormaPagamentoViewSet
from .views.view_usuario import  UsuarioViewSet

router = DefaultRouter()
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'forma_pagamento', FormaPagamentoViewSet)
router.register(r'usuarios', UsuarioViewSet)
urlpatterns = [
    path('', include(router.urls)),
    
]
