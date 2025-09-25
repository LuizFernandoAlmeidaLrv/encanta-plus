from rest_framework import viewsets
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)
from datetime import date
from pedido.models.model_pedido import Pedido, Cliente, Produto, Composicao,  Cardapio, CardapioIngredientes, Ingrediente
from cadastro.models import  FormaPagamento, ListaItem
from pedido.serializers.serializer_pedido import PedidoSerializer, PedidoSerializer2, ProdutoSerializer, ComposicaoSerializer, PedidoItemSerializer,PedidoItemComposicaoSerializer
from cadastro.serializers import ClienteSerializer, FormaPagamentoSerializer, ListaItemSerializer

class ListaItemViewSet(viewsets.ModelViewSet):
    queryset = ListaItem.objects.all()
    serializer_class = ListaItemSerializer

    def list(self, request):
        lista_id = request.GET.get("lista_id", None)  # Filtro por lista específica
        if lista_id:
            queryset = self.queryset.filter(lista_id=lista_id)
        else:
            queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def list(self, request, *args, **kwargs):
        telefone = request.GET.get("telefone", None)

        if telefone:
            clientes = Cliente.objects.filter(telefone=telefone)  # Busca EXATA
            if clientes.exists():
                serializer = self.get_serializer(clientes, many=True)
                return Response(serializer.data)
            else:
                return Response([], status=status.HTTP_200_OK)  # Retorna array vazio corretamente
        
        return super().list(request, *args, **kwargs)  # Retorna todos se não houver filtro



class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()  # Aqui o queryset é necessário
    serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    print("\n🔹 RECEBENDO REQUISIÇÃO PARA consultar PEDIDO..." , queryset)
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        print("\n🔹 RECEBENDO REQUISIÇÃO PARA CRIAR PEDIDO...")
        print("📌 Dados recebidos:", request.data)  # Mostra os dados enviados no request
        
        logger.debug("Método create chamado com os dados: %s", request.data)

        pedido_data = request.data
        pedido_serializer = PedidoSerializer2(data=pedido_data)

        if pedido_serializer.is_valid():
            pedido = pedido_serializer.save()  # Salva o Pedido
            print("✅ Pedido salvo com sucesso! ID:", pedido.numero_pedido)

            # Criar os itens do pedido
            
            itens_pedido_data = pedido_data.get("itens", [])
            for item_data in itens_pedido_data:
                # Aqui você já tem a instância do Pedido
                item_data["pedido"] = pedido.numero_pedido  # Agora passamos o ID diretamente
                item_serializer = PedidoItemSerializer(data=item_data)

                if item_serializer.is_valid():
                    item = item_serializer.save()  # Salva o PedidoItem
                    print(f"✅ PedidoItem salvo com sucesso! ID: {item.id}")

                    # Se for uma marmita, adicionar a composição
                    if item_data.get("eh_marmita", False):
                        composicao_data = item_data.get("composicao", [])
                        for comp_data in composicao_data:
                            comp_data["pedido_item"] = item  # Aqui também passando a instância do PedidoItem
                            comp_serializer = PedidoItemComposicaoSerializer(data=comp_data)

                            if comp_serializer.is_valid():
                                comp_serializer.save()  # Salva a composição
                                print(f"✅ Composição salva com sucesso para o item {item.id}")
                            else:
                                print(f"❌ Erro ao salvar composição: {comp_serializer.errors}")

                else:
                    print(f"❌ Erro ao salvar PedidoItem: {item_serializer.errors}")

            return Response(PedidoSerializer2(pedido).data, status=status.HTTP_201_CREATED)

        # Caso tenha erro na criação do pedido
        print("❌ Erros de validação jesus:", pedido_serializer.errors)
        return Response(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer


class ComposicaoViewSet(viewsets.ViewSet):
    """
    Viewset para listar a composição dos produtos.
    """

    def retrieve(self, request, pk=None):
        try:
            # Tenta pegar o produto
            produto = Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            return Response({"detail": "Produto não encontrado."}, status=404)

        # Utiliza o ProdutoSerializer para buscar os ingredientes do produto
        produto_serializado = ProdutoSerializer(produto)
        print("❌ Erros de validação:", produto_serializado.data)
        # Pega os ingredientes do produto já processados no serializer
        ingredientes = produto_serializado.data.get('ingredientes', [])

        return Response({
            "produto": produto_serializado.data,
            "composicao": ingredientes
        })