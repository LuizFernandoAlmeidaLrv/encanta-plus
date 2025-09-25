from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

from suprimentos.models.nota_fiscal_entrada import NotaFiscalEntrada
from suprimentos.serializers.nota_fiscal_entrada_serializer import NotaFiscalEntradaSerializer
from suprimentos.services.estoque import gerar_movimentos_estoque
from suprimentos.services.custo import criar_custo_automatico

# Importa a view onde está o método

class NotaFiscalEntradaViewSet(viewsets.ModelViewSet):
    queryset = NotaFiscalEntrada.objects.all()
    serializer_class = NotaFiscalEntradaSerializer

    @action(detail=True, methods=['post'])
    def fechar(self, request, pk=None):
        nota = self.get_object()

        if nota.situacao != '1':
            return Response({'detail': 'Nota já foi fechada ou cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

        nota.situacao = '2'
        nota.save()

        try:
            gerar_movimentos_estoque(nota, tipo="E")
        except Exception as e:
            return Response({'detail': f'Erro ao gerar movimentos de estoque: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        erros = []
        for item in nota.itens.all():
            print("Itens da nota:", list(nota.itens.all()))
            print(f"Item: {item}, aplicar_custo: {item.aplicar_custo}")

            try:
                frete_percentual = item.percentual_frete or 0
                valor_unit = item.valor_unitario or 0
                valor_frete = (valor_unit * frete_percentual) / 100
                valor_final = valor_unit + valor_frete

                # Usa o método do ViewSet diretamente
                criar_custo_automatico(
                    item_nf={
                        'produto': item.produto.codigo,
                        'data_custo': nota.data_entrada,
                        'hora_custo': 0,
                        'valor_base': valor_unit,
                        'perc_frete': frete_percentual,
                        'valor_frete': valor_frete,
                        'valor_custo': valor_final,
                        'numero_nota': nota.numero,
                        'serie_nota': nota.serie,
                        'seq_item': item.id,
                        'cod_fornecedor': nota.fornecedor.id,
                    },
                    usuario=request.user
                )

            except Exception as e:
                erros.append(f"Erro no produto {item.produto}: {str(e)}")

        if erros:
            return Response({
                'detail': 'Nota fechada com alertas.',
                'erros_custos': erros
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response({'detail': 'Nota fechada com sucesso e custos gerados!'})
