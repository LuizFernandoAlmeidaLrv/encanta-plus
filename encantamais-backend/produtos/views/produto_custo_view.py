from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from produtos.models.produtocusto import ProdutoCusto
from produtos.models.produto import Produto
from produtos.serializers.serializer_custo import ProdutoCustoSerializer


class ProdutoCustoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoCusto.objects.all()
    serializer_class = ProdutoCustoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        situacao = request.query_params.get('situacao')
        if situacao:
            queryset = queryset.filter(situacao=situacao)

        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            print("Primeiro custo serializado para debug:", serializer.data[0])
        else:
            print("Nenhum custo retornado.")

        return Response(serializer.data)

    
    
    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        ultima_sequencia = (
            ProdutoCusto.objects
            .filter(produto=produto)
            .order_by('-sequencia')
            .values_list('sequencia', flat=True)
            .first()
        )
        nova_sequencia = (ultima_sequencia or 0) + 1
        serializer.save(
            sequencia=nova_sequencia,
            usuario_gerador=self.request.user  # Aqui salva corretamente o usuário logado
        )

    @action(detail=False, methods=['post'])
    def processar(self, request):
        produto = request.data.get('produto')  # aqui você deve passar o código do produto
        data_custo = request.data.get('data_custo')
        sequencia = request.data.get('sequencia')

        if not produto or not data_custo or sequencia is None:
            return Response({'erro': 'Parâmetros insuficientes.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            custo = ProdutoCusto.objects.get(
                produto__codigo=produto,
                data_custo=data_custo,
                sequencia=sequencia
            )

            if custo.atualiza_custo_preco == 'S':
                produto_obj = Produto.objects.get(codigo=produto)
                produto_obj.custo_medio = custo.custo_medio
                produto_obj.save()

            custo.situacao = 'P'
            custo.save()

            return Response({'mensagem': 'Custo processado com sucesso.'})

        except ProdutoCusto.DoesNotExist:
            return Response({'erro': 'Custo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'])
    def processar_em_lote(self, request):
        chaves = request.data.get('chaves', [])
        print("Recebendo chaves para processamento:", chaves)

        erros = []
        sucesso = 0

        for chave in chaves:
            try:
                custo = ProdutoCusto.objects.get(
                    produto__codigo=chave['produto'],
                    data_custo=chave['data_custo'],
                    sequencia=chave['sequencia']
                )

                if custo.atualiza_custo_preco == 'S':
                    produto = Produto.objects.get(codigo=chave['produto'])
                    produto.custo_medio = custo.custo_medio
                    produto.save()

                custo.situacao = 'P'
                custo.save()
                sucesso += 1

            except Exception as e:
                erros.append(f"Erro para {chave}: {str(e)}")

        return Response({
            'mensagem': f'{sucesso} custos processados com sucesso.',
            'falhas': erros
        })
