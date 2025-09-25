from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from produtos.models.produto import Produto
from produtos.models.produtocusto import ProdutoCusto


class UltimoCustoAPIView(APIView):
    def get(self, request, produto_id):
        try:
            # Busca o produto pelo código (PK)
            produto = Produto.objects.get(codigo=produto_id)
        except Produto.DoesNotExist:
            return Response({"detail": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Busca o último custo registrado para o produto
        ultimo_custo = ProdutoCusto.objects.filter(produto=produto).order_by('-data_geracao').first()

        if not ultimo_custo:
            return Response({
                "custo_anterior": None,
                "custo_atual": None,
                "custo_medio": None,
                "valor_base_anterior": None,
                "valor_base_atual": None,
            }, status=status.HTTP_200_OK)

        return Response({
            "custo_anterior": None,  # Você pode ajustar se tiver esse dado em outra tabela
            "custo_atual": ultimo_custo.valor_custo,
            "custo_medio": ultimo_custo.custo_medio,
            "valor_base_anterior": None,
            "valor_base_atual": ultimo_custo.valor_base,
            "valor_frete": ultimo_custo.valor_frete,
        }, status=status.HTTP_200_OK)
