from rest_framework import viewsets
from ..models.model_caixa import Caixa
from ..serializers.serializer_caixa import CaixaSerializer

class CaixaStatusViewSet(viewsets.ModelViewSet):
    queryset = Caixa.objects.all()
    serializer_class = CaixaSerializer

    def retrieve(self, request, *args, **kwargs):
        # Lógica personalizada para obter o status do caixa
        caixa = self.get_object()
        return Response({'status': caixa.status})  # Supondo que o modelo Caixa tenha um campo status
