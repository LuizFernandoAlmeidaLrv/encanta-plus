from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from produtos.models.produto import Produto
from preco.models.tabela_preco import  TabelaPreco
from preco.models.formacao_preco import  FormacaoPreco, FormacaoPrecoHistorico
from preco.models.tabela_preco_produto import TabelaPrecoProduto

from preco.serializers.serializers_preco import (
    TabelaPrecoSerializer,
    FormacaoPrecoSerializer,
    TabelaPrecoProdutoSerializer,
    HistoricoFormacaoPrecoSerializer,
)

class TabelaPrecoViewSet(viewsets.ModelViewSet):
    queryset = TabelaPreco.objects.all()
    serializer_class = TabelaPrecoSerializer

class FormacaoPrecoViewSet(viewsets.ModelViewSet):
    queryset = FormacaoPreco.objects.select_related("produto").all()
    serializer_class = FormacaoPrecoSerializer
    lookup_field = 'produto_id'  # <- Isso faz o endpoint funcionar com o código do produto na URL


class TabelaPrecoProdutoViewSet(viewsets.ModelViewSet):
    queryset = TabelaPrecoProduto.objects.all()
    serializer_class = TabelaPrecoProdutoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        produto = data.get('produto')
        tabela = data.get('tabela_preco')
        data_inicial = data.get('data_inicial')

        if not (produto and tabela and data_inicial):
            return Response(
                {"detail": "Campos obrigatórios ausentes: produto, tabela_preco, data_inicial"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instancia_existente = TabelaPrecoProduto.objects.filter(
            produto=produto,
            tabela_preco=tabela,
            data_inicial=data_inicial
        ).first()

        if instancia_existente:
            # Atualiza os campos permitidos
            serializer = self.get_serializer(instancia_existente, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Cria novo
            return super().create(request, *args, **kwargs)


class HistoricoFormacaoPrecoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FormacaoPrecoHistorico.objects.all().order_by('-data_alteracao')
    serializer_class = HistoricoFormacaoPrecoSerializer

class FormacaoPrecoByProdutoAPIView(APIView):
    def get(self, request, produto_id):
        try:
            # Primeiro tenta buscar o produto
            produto = Produto.objects.get(codigo=produto_id)

            try:
                # Se o produto existe, tenta buscar a formação de preço
                formacao = FormacaoPreco.objects.get(produto=produto)
                serializer = FormacaoPrecoSerializer(formacao)
                return Response(serializer.data)

            except FormacaoPreco.DoesNotExist:
                # Produto existe, mas não tem formação de preço ainda
                return Response({
                    "codigo_produto": produto.codigo,
                    "nome_produto": produto.nome,
                    "valor_custo": None,
                    "margem_lucro": None,
                    "valor_venda": None
                }, status=status.HTTP_200_OK)

        except Produto.DoesNotExist:
            # Produto não encontrado
            return Response({"detail": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)