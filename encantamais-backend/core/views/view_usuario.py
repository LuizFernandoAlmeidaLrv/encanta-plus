# financeiro/views/view_usuario.py
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from core.models import Usuario
from core.serializers.serializer_usuario import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by("username")
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # só admin cadastra

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retorna os dados do usuário logado"""
        user = request.user
        try:
            usuario = Usuario.objects.get(pk=user.id)
            return Response({
                "id": usuario.id,
                "nome": usuario.username,
                "email": getattr(usuario, "email", None),
                "tipo": getattr(usuario, "tipo", None),
            }, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
