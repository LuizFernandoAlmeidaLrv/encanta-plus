# vendas/views/venda.py
from rest_framework import viewsets, status
from django.db import transaction
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware, get_default_timezone
from vendas.models.models_venda import Venda, VendaItem
from vendas.models.models_venda_parcela import VendaParcela
from vendas.serializers.serializers_venda import VendaSerializer, VendaItemSerializer, VendaParcelaSerializer
from financeiro.models.models_titulo_receber import TituloReceber
from financeiro.models.models_titulo_movimento import TituloMovimento
from suprimentos.services.estoque import gerar_movimentos_estoque
from financeiro.serializers.serializers_titulo_receber import TituloReceberSerializer, TituloMovimentoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        p = self.request.query_params
        tz = get_default_timezone()  # timezone do Django

        situacao = p.get("situacao")
        if situacao:
            qs = qs.filter(situacao=situacao)
    
        tipo = p.get("tipo")
        if tipo:
            qs = qs.filter(tipo=tipo)

        id = p.get("id")
        if id:
            qs = qs.filter(id=id)
    
        cliente_id = p.get("cliente")
        if cliente_id:
            qs = qs.filter(cliente_id=cliente_id)
    
    # --- Datas da venda ---
        data_ini = p.get("data_venda__gte")
        if data_ini:
            try:
                dt_ini = datetime.strptime(data_ini, "%Y-%m-%d")
                dt_ini = make_aware(datetime.combine(dt_ini.date(), time.min), tz)
                qs = qs.filter(data_venda__gte=dt_ini)
            except ValueError:
                pass

        data_fim = p.get("data_venda__lte")
        if data_fim:
            try:
                dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")
                dt_fim = make_aware(datetime.combine(dt_fim.date(), time.max), tz)
                qs = qs.filter(data_venda__lte=dt_fim)
            except ValueError:
                pass

        # --- Datas da liberação ---
        data_libini = p.get("data_liberacao__gte")
        if data_libini:
            try:
                dt_libini = datetime.strptime(data_libini, "%Y-%m-%d")
                dt_libini = make_aware(datetime.combine(dt_libini.date(), time.min), tz)
                qs = qs.filter(data_liberacao__gte=dt_libini)
            except ValueError:
                pass

        data_libfim = p.get("data_liberacao__lte")
        if data_libfim:
            try:
                dt_libfim = datetime.strptime(data_libfim, "%Y-%m-%d")
                dt_libfim = make_aware(datetime.combine(dt_libfim.date(), time.max), tz)
                qs = qs.filter(data_liberacao__lte=dt_libfim)
            except ValueError:
                pass

        usuario = p.get("usuario")
        if usuario:
            qs = qs.filter(usuario_id=usuario)

        print("\n--- Dados recebidos venda ---")
        print(qs.query)  # SQL para debug
        print("----------------------------------------\n")

        return qs.order_by("-data_venda")

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Cria a venda
            venda_serializer = self.get_serializer(data=request.data)
            venda_serializer.is_valid(raise_exception=True)
            venda = venda_serializer.save()
        
            # Cria os itens da venda
            itens_data = request.data.get("itens", [])
            for item in itens_data:
                item["venda"] = venda.id
                item_serializer = VendaItemSerializer(data=item)
                item_serializer.is_valid(raise_exception=True)
                item_serializer.save()

            # Cria as parcelas da venda
            parcelas_data = request.data.get("parcelas", [])
            for parcela in parcelas_data:
                parcela["venda"] = venda.id
                parcela_serializer = VendaParcelaSerializer(data=parcela)
                parcela_serializer.is_valid(raise_exception=True)
                parcela_serializer.save()

            return Response(self.get_serializer(venda).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def liberar(self, request, pk=None):
        print("\n--- Dados recebidos no liberar_venda ---")
        print(request.data)
        print("----------------------------------------\n")
        """
        Libera a venda:
          - cria TituloReceber para cada VendaParcela da venda
          - cria um TituloMovimento tipo 'E' para cada título (lançamento)
          - altera venda.situacao para 'LI' (Liberada)
        """
        venda = self.get_object()
        print("\n--- Dados recebidos no liberar_venda (venda) ---")
        print("ID:", venda.id)
        print("Cliente ID:", venda.cliente_id)
        print("Cliente:", venda.cliente)  # Isso vai acessar o FK e trazer o objeto, se houver
        print("Situação:", venda.situacao)
        print("Data venda:", venda.data_venda)
        print("Itens:", list(venda.itens.all()))
        print("Data venda:", venda.data_venda)
        # Checagens básicas (ajuste conforme suas regras)
        if venda.situacao == 'CA':  # cancelada
            return Response({"detail": "Venda cancelada não pode ser liberada."}, status=status.HTTP_400_BAD_REQUEST)
        if venda.situacao == 'LI':
            return Response({"detail": "Venda já liberada."}, status=status.HTTP_400_BAD_REQUEST)

        # Busca parcelas vinculadas à venda
        parcelas = VendaParcela.objects.filter(venda=venda).order_by('numero_parcela')
        if not parcelas.exists():
            return Response({"detail": "Nenhuma parcela encontrada para esta venda."}, status=status.HTTP_400_BAD_REQUEST)

        created_titulos = []

        try:
            with transaction.atomic():
                # Cria títulos a partir das parcelas
                for parcela in parcelas:
                    print("Parcela:", parcela.id, "Forma pgto:", parcela.forma_pagamento_id, "data_vencimento", parcela.data_vencimento)
                    titulo_data = {
                        'venda': venda.id,
                        'cliente': venda.cliente_id, 
                        'valor': parcela.valor_parcela,   # adapte se o campo tiver outro nome
                        'forma_pagamento_id': parcela.forma_pagamento_id,
                        'data_vencimento': parcela.data_vencimento,
                        'situacao': 'A',  # Aberto
                        'observacao': getattr(parcela, 'observacao', '') or getattr(venda, 'observacao', '')
                    }
                    titulo_serializer = TituloReceberSerializer(data=titulo_data)
                    titulo_serializer.is_valid(raise_exception=True)
                    titulo = titulo_serializer.save()
                    created_titulos.append(titulo)

                    # Cria movimento do tipo 'E' (lançamento / entrada na criação)
                    print("Parcelaitem:", parcela.id, "Forma pgto:", parcela.forma_pagamento_id)
                    movimento_data = {
                        'titulo_receber': titulo.id,
                        'tipo': 'E',  # 'E' = lançamento/entrada (conforme sua convenção)
                        'valor': titulo.valor,
                        'forma_pagamento_id': titulo.forma_pagamento_id,
                        'data_movimento': timezone.now().date(),
                        'observacao': f'Geração automática ao liberar venda #{venda.id}'
                        # 'usuario': request.user.id  # opcional: se seu modelo usar usuário
                    }
                    mov_serializer = TituloMovimentoSerializer(data=movimento_data)
                    mov_serializer.is_valid(raise_exception=True)
                    mov_serializer.save()

                try:
                    gerar_movimentos_estoque(venda, tipo="S")
                except Exception as e:
                    return Response({'detail': f'Erro ao gerar movimentos de estoque: {str(e)}'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Atualiza situação da venda para Liberada                
                venda.situacao = 'LI'
                venda.save()
               
                
            # Serializa resposta com os títulos gerados
            resp = TituloReceberSerializer(created_titulos, many=True).data
            return Response({'detail': 'Venda liberada com sucesso', 'titulos': resp}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # O atomic garante rollback automático, aqui só reportamos
            return Response({'detail': 'Erro ao liberar venda', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VendaItemViewSet(viewsets.ModelViewSet):
    queryset = VendaItem.objects.all()
    serializer_class = VendaItemSerializer


class VendaParcelaViewSet(viewsets.ModelViewSet):
    queryset = VendaParcela.objects.all()
    serializer_class = VendaParcelaSerializer
