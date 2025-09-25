# financeiro/models/models_caixa.py
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from core.models import FormaPagamento, Usuario
from financeiro.models import TituloMovimento
from django.utils import timezone

User = get_user_model()

SITUACAO_CAIXA = (
    ('A', 'Aberto'),
    ('F', 'Fechado'),
)

TIPO_MOVIMENTO = (
    ('E', 'Entrada'),
    ('S', 'Saída'),
)

class Caixa(models.Model):
    data_caixa = models.DateField(unique=True)
    data_abertura_caixa = models.DateTimeField(auto_now_add=True)
    data_fechamento_caixa = models.DateTimeField(null=True, blank=True)
    usuario_abertura = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, related_name="caixas_abertos"
    )
    usuario_fechamento = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, null=True, blank=True, related_name="caixas_fechados"
    )
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Totais agregados
    total_entradas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_saidas = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Totais por forma de pagamento
    total_dinheiro = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cartao_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cartao_debito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_pix = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  
    diferenca = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # diferença caixa x físico

    situacao = models.CharField(max_length=1, choices=SITUACAO_CAIXA, default='A')

    def __str__(self):
        return f'Caixa {self.data_caixa} - {self.get_situacao_display()}'
   
    def fechar(self):
        self.data_fechamento_caixa = timezone.now()
        self.save()

class CaixaMovimento(models.Model):
    CAIXA_TIPO = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    caixa = models.ForeignKey('Caixa', on_delete=models.CASCADE, related_name='movimentos')
    tipo = models.CharField(max_length=1, choices=CAIXA_TIPO)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    historico = models.TextField(blank=True, null=True)
    titulo_movimento = models.ForeignKey(TituloMovimento, blank=True, null=True, on_delete=models.SET_NULL)
    data_movimento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        caixa = self.caixa

        total_entradas = caixa.movimentos.filter(tipo="E").aggregate(total=Sum("valor"))["total"] or 0
        total_saidas = caixa.movimentos.filter(tipo="S").aggregate(total=Sum("valor"))["total"] or 0

        # Atualiza saldo atual
        caixa.saldo_atual = caixa.saldo_inicial + total_entradas - total_saidas
        caixa.total_entradas = total_entradas
        caixa.total_saidas = total_saidas

        # Atualiza totais por forma de pagamento (exemplo com IDs fixos)
        caixa.total_dinheiro = caixa.movimentos.filter(forma_pagamento__id=1, tipo='E').aggregate(total=Sum('valor'))['total'] or 0
        caixa.total_cartao_credito = caixa.movimentos.filter(forma_pagamento__id=2, tipo='E').aggregate(total=Sum('valor'))['total'] or 0
        caixa.total_cartao_debito = caixa.movimentos.filter(forma_pagamento__id=3, tipo='E').aggregate(total=Sum('valor'))['total'] or 0
        caixa.total_pix = caixa.movimentos.filter(forma_pagamento__id=4, tipo='E').aggregate(total=Sum('valor'))['total'] or 0

        caixa.save(update_fields=[
            "saldo_atual", "total_entradas", "total_saidas",
            "total_dinheiro", "total_cartao_credito", "total_cartao_debito", "total_pix"
        ])
