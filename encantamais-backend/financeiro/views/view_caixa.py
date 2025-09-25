# financeiro/views/view_caixa.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta

from financeiro.models.models_titulo_receber import TituloReceber
from financeiro.models.models_titulo_movimento import TituloMovimento
from financeiro.models.models_caixa import Caixa, CaixaMovimento
from financeiro.serializers.serializers_caixa import CaixaSerializer, CaixaMovimentoSerializer
from core.models import FormaPagamento


class CaixaViewSet(viewsets.ModelViewSet):
    queryset = Caixa.objects.all().order_by("-data_caixa")
    serializer_class = CaixaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def abrir_primeiro(self, request):
        """Abre o primeiro caixa do sistema"""
        if Caixa.objects.filter(situacao="A").exists():
            return Response({"detail": "Já existe um caixa aberto"}, status=status.HTTP_400_BAD_REQUEST)

        usuario_id = request.data.get("usuario_abertura")
        saldo_inicial = request.data.get("saldo_inicial", 0)

        try:
            caixa = Caixa.objects.create(
                data_caixa=timezone.localdate(),
                saldo_inicial=saldo_inicial,
                situacao="A",
                usuario_abertura_id=usuario_id,
            )
            # Cria movimento de entrada do saldo inicial
            CaixaMovimento.objects.create(
                caixa=caixa,
                tipo="E",
                valor=saldo_inicial,
                forma_pagamento_id=1,  # Dinheiro
                historico="Saldo inicial",
                usuario_id=usuario_id,
            )
            return Response(CaixaSerializer(caixa).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def fechar(self, request, pk=None):
        try:
            caixa = self.get_object()
            if caixa.situacao != 'A':
                return Response({"detail": "Caixa não está aberto"}, status=status.HTTP_400_BAD_REQUEST)

            # recalcula totais a partir dos movimentos já salvos
            total_entradas = caixa.movimentos.filter(tipo="E").aggregate(total=Sum("valor"))["total"] or 0
            total_saidas = caixa.movimentos.filter(tipo="S").aggregate(total=Sum("valor"))["total"] or 0

            # atualiza campos do caixa
            caixa.total_entradas = total_entradas
            caixa.total_saidas = total_saidas
            caixa.saldo_final = (caixa.saldo_inicial or 0) + total_entradas - total_saidas
            caixa.usuario_fechamento = request.user          # <-- usa o usuário autenticado
            caixa.data_fechamento_caixa = timezone.now()
            caixa.situacao = 'F'
            caixa.save(update_fields=[
                "total_entradas",
                "total_saidas",
                "saldo_final",
                "usuario_fechamento",
                "data_fechamento_caixa",
                "situacao",
            ])

            # opcional: abrir novo caixa automaticamente se solicitado
            abrir_novo = request.data.get("abrir_novo", False)
            if abrir_novo:
                # se o frontend passar uma data para o novo caixa, tenta usar; senão usa próximo dia
                data_novo_str = request.data.get("data_novo_caixa")
                if data_novo_str:
                    try:
                        data_novo = datetime.strptime(data_novo_str, "%Y-%m-%d").date()
                    except ValueError:
                        return Response({"detail": "data_novo_caixa inválida. Formato esperado: YYYY-MM-DD."},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    data_novo = caixa.data_caixa + timedelta(days=1)

                # verifica existência
                if Caixa.objects.filter(data_caixa=data_novo).exists():
                    # Se já existir, não criar — somente informa no retorno
                    novo_caixa = None
                    msg = "Caixa fechado. Novo caixa não criado porque já existe para a data solicitada."
                else:
                    novo_caixa = Caixa.objects.create(
                        data_caixa=data_novo,
                        usuario_abertura=request.user,     # usa request.user
                        saldo_inicial=caixa.saldo_final or 0,
                        situacao='A',
                    )
                    msg = "Caixa fechado e novo caixa aberto."

                # serializa resposta incluindo o novo caixa (se criado)
                data_response = {
                    "detail": msg,
                    "caixa_fechado": CaixaSerializer(caixa).data,
                    "novo_caixa": CaixaSerializer(novo_caixa).data if novo_caixa else None,
                }
                return Response(data_response, status=status.HTTP_200_OK)

            # se não pediu para abrir novo, retorna apenas o caixa fechado
            return Response({"detail": "Caixa fechado com sucesso.", "caixa": CaixaSerializer(caixa).data},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        qs = super().get_queryset()
        p = self.request.query_params

        situacao = p.get("situacao")
        if situacao:
            qs = qs.filter(situacao=situacao)

        data_ini = p.get("data_caixa__gte")
        if data_ini:
            qs = qs.filter(data_caixa__gte=data_ini)

        data_fim = p.get("data_caixa__lte")
        if data_fim:
            qs = qs.filter(data_caixa__lte=data_fim)

        usuario = p.get("usuario")
        if usuario:
            qs = qs.filter(usuario_abertura_id=usuario)

        return qs.order_by("-data_caixa")

class CaixaMovimentoViewSet(viewsets.ModelViewSet):
    queryset = CaixaMovimento.objects.all().order_by('-data_movimento')
    serializer_class = CaixaMovimentoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        caixa_id = self.request.query_params.get("caixa")
        if caixa_id:
            queryset = queryset.filter(caixa_id=caixa_id)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            movimento = serializer.save()
            return Response(self.get_serializer(movimento).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Melhor ser APIView isolada para a baixa
from rest_framework.views import APIView
class BaixarTitulosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        parcelas_data = request.data.get("parcelas", [])
        if not parcelas_data:
            return Response({"detail": "Nenhuma parcela enviada."},
                            status=status.HTTP_400_BAD_REQUEST)

        # busca caixa aberto do dia
        caixa_aberto = Caixa.objects.filter(
            data_caixa=timezone.localdate(),
            situacao="A"
        ).first()
        if not caixa_aberto:
            return Response({"detail": "Não existe caixa aberto para hoje."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for parcela_info in parcelas_data:
                    parcela_id = parcela_info.get("id")
                    pagamentos = parcela_info.get("pagamentos", [])

                    if not pagamentos:
                        return Response({"detail": f"Parcela {parcela_id}: informe ao menos um pagamento."},
                                        status=status.HTTP_400_BAD_REQUEST)

                    try:
                        parcela = (TituloReceber.objects
                                   .select_for_update()
                                   .get(pk=parcela_id))
                    except TituloReceber.DoesNotExist:
                        return Response({"detail": f"Parcela {parcela_id} não encontrada."},
                                        status=status.HTTP_404_NOT_FOUND)

                    # já paga?
                    if getattr(parcela, "situacao", None) == "P":
                        return Response({"detail": f"Parcela {parcela_id} já está paga."},
                                        status=status.HTTP_400_BAD_REQUEST)

                    total_pg = 0.0

                    for pg in pagamentos:
                        # aceita "forma", "forma_pagamento" ou "forma_pagamento_id"
                        forma_id = (pg.get("forma_pagamento")
                                    or pg.get("forma")
                                    or pg.get("forma_pagamento_id"))
                        valor = pg.get("valor", 0)

                        try:
                            valor = float(valor)
                        except (TypeError, ValueError):
                            valor = 0.0

                        if not forma_id or valor <= 0:
                            # ignora linhas inválidas
                            continue

                        forma = FormaPagamento.objects.get(pk=forma_id)

                        # 1) movimento de TÍTULO — **um por pagamento**
                        TituloMovimento.objects.create(
                            # ATENÇÃO: ajuste o nome do FK conforme seu modelo:
                            # se for 'parcela', troque para parcela=parcela
                            # se for 'titulo_receber', troque para titulo_receber=parcela
                            titulo_receber_id=parcela_id,
                            tipo="B",
                            valor=valor,
                            forma_pagamento_id=forma_id,
                            data_movimento=timezone.localdate(),
                            observacao=f"Baixa via {getattr(forma, 'descricao', str(forma_id))}",
                        )

                        # 2) movimento de CAIXA — **um por pagamento**
                        CaixaMovimento.objects.create(
                            caixa=caixa_aberto,
                            tipo="E",  # Entrada
                            valor=valor,
                            forma_pagamento=forma,
                            historico=f"Baixa Título {parcela.id}",
                            data_movimento=timezone.localdate(),
                            usuario=request.user,
                        )

                        total_pg += valor

                    if total_pg <= 0:
                        return Response({"detail": f"Nenhum pagamento válido informado para a parcela {parcela_id}."},
                                        status=status.HTTP_400_BAD_REQUEST)

                    # regra simples: se total pago cobre o valor da parcela, marca como paga
                    try:
                        valor_parcela = float(getattr(parcela, "valor", 0) or 0)
                    except (TypeError, ValueError):
                        valor_parcela = 0.0

                    if total_pg >= valor_parcela:
                        parcela.situacao = "P"
                        parcela.data_recebimento = timezone.localdate()
                        parcela.save(update_fields=["situacao", "data_recebimento"])
                    else:
                        # mantém em aberto (ou marque como 'PAR' se existir esse status)
                        parcela.data_recebimento = timezone.localdate()
                        parcela.save(update_fields=["data_recebimento"])

            return Response({"detail": "Baixa efetuada com sucesso."},
                            status=status.HTTP_200_OK)

        except FormaPagamento.DoesNotExist:
            return Response({"detail": "Forma de pagamento inválida."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)