from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.model_contas_receber import TituloReceber, TituloMovimento, TituloHistorico
from ..serializers.serializer_contas_receber import (
    TituloReceberSerializer,
    TituloMovimentoSerializer,
    TituloHistoricoSerializer,
)

# ViewSet para Títulos a Receber
class TituloReceberViewSet(viewsets.ModelViewSet):
    queryset = TituloReceber.objects.all().order_by('-data_emissao')
    serializer_class = TituloReceberSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario_criacao=self.request.user)
        else:
            # Se não houver usuário logado, pode lançar um erro ou atribuir um valor padrão
            raise ValueError("Usuário não autenticado.")


# ViewSet para Movimentos dos Títulos
class TituloMovimentoViewSet(viewsets.ModelViewSet):
    queryset = TituloMovimento.objects.all().order_by('-data')
    serializer_class = TituloMovimentoSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para Histórico de Títulos
class TituloHistoricoViewSet(viewsets.ModelViewSet):
    queryset = TituloHistorico.objects.all().order_by('-data')
    serializer_class = TituloHistoricoSerializer
    permission_classes = [IsAuthenticated]
