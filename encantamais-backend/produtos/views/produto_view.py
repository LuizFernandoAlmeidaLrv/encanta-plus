from django.db.models import Max, Prefetch, Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from produtos.models.produto import Produto
from preco.models.tabela_preco_produto import TabelaPrecoProduto
from produtos.serializers.produto_serializer import ProdutoSerializer
from produtos.serializers.produto_serializer import ProdutoSerializer

@api_view(['GET'])
def buscar_produto_por_codigo(request, codigo):
    try:
        produto = Produto.objects.get(codigo=codigo)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    except Produto.DoesNotExist:
        return Response({'detail': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class ProdutoViewSet(viewsets.ModelViewSet):
    hoje = date.today()
    queryset = Produto.objects.all().prefetch_related(
        Prefetch(
            'tabelaprecoproduto_set',  # ou o related_name correto do seu FK
            queryset=TabelaPrecoProduto.objects.filter(
                data_inicial__lte=hoje
            ).filter(
                Q(data_final__gte=hoje) | Q(data_final__isnull=True)
            ),
            to_attr='precos_validos'
        )
    )
    serializer_class = ProdutoSerializer

    def perform_create(self, serializer):
        codigo = self.request.data.get('codigo', '').strip()

        if not codigo:
            ultimo = Produto.objects.aggregate(maior=Max('codigo'))['maior']
            if ultimo and str(ultimo).isdigit():
                novo_codigo = str(int(ultimo) + 1).zfill(6)
            else:
                novo_codigo = '000001'
            serializer.save(codigo=novo_codigo)
        else:
            serializer.save()