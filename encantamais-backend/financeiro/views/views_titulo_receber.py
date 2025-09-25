from rest_framework import viewsets
from django.utils.timezone import make_aware, get_default_timezone
from datetime import datetime, time
from financeiro.models.models_titulo_receber import TituloReceber
from financeiro.serializers.serializers_titulo_receber import TituloReceberSerializer


class TituloReceberViewSet(viewsets.ModelViewSet):
    queryset = TituloReceber.objects.all()
    serializer_class = TituloReceberSerializer

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

        # --- Datas da Venda (vem da relação com Venda) ---
        data_ini = p.get("data_venda__gte")
        if data_ini:
            try:
                dt_ini = datetime.strptime(data_ini, "%Y-%m-%d")
                dt_ini = make_aware(datetime.combine(dt_ini.date(), time.min), tz)
                qs = qs.filter(venda__data_venda__gte=dt_ini)
            except ValueError:
                pass

        data_fim = p.get("data_venda__lte")
        if data_fim:
            try:
                dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")
                dt_fim = make_aware(datetime.combine(dt_fim.date(), time.max), tz)
                qs = qs.filter(venda__data_venda__lte=dt_fim)
            except ValueError:
                pass

        # --- Datas de Vencimento ---
        data_venini = p.get("data_vencimento__gte")
        if data_venini:
            try:
                dt_venini = datetime.strptime(data_venini, "%Y-%m-%d")
                dt_venini = make_aware(datetime.combine(dt_venini.date(), time.min), tz)
                qs = qs.filter(data_vencimento__gte=dt_venini)
            except ValueError:
                pass

        data_venfim = p.get("data_vencimento__lte")
        if data_venfim:
            try:
                dt_venfim = datetime.strptime(data_venfim, "%Y-%m-%d")
                dt_venfim = make_aware(datetime.combine(dt_venfim.date(), time.max), tz)
                qs = qs.filter(data_vencimento__lte=dt_venfim)
            except ValueError:
                pass

        usuario = p.get("usuario")
        if usuario:
            qs = qs.filter(usuario_id=usuario)

        print("\n--- Dados Titulo Receber ---")
        print(qs.query)  # SQL para debug
        print("----------------------------------------\n")

        return qs.order_by("-data_movimento")
