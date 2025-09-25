from django.db import models
from django.conf import settings
from preco.models.tabela_preco import TabelaPreco
from produtos.models.produto import Produto  # ajuste conforme necessário

class TabelaPrecoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tabela_preco = models.ForeignKey(TabelaPreco, on_delete=models.CASCADE)

    preco_venda = models.DecimalField("Preço de Venda", max_digits=10, decimal_places=4)
    data_inicial = models.DateField("Início da Vigência")
    data_final = models.DateField("Fim da Vigência", blank=True, null=True)

    # Novos campos importantes:
    valor_custo = models.DecimalField("Valor do Custo", max_digits=10, decimal_places=4, default=0)
    margem_lucro = models.DecimalField("Margem de Lucro (%)", max_digits=6, decimal_places=2, default=0)
    margem_custo_fixo = models.DecimalField("Margem Custo Fixo (%)", max_digits=6, decimal_places=2, default=0)
    custo_base = models.DecimalField("Custo Base", max_digits=10, decimal_places=4, default=0)
    custo_com_frete = models.DecimalField("Custo com Frete", max_digits=10, decimal_places=4, default=0)

    # Controle de auditoria:
    usuario_criacao = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="tabela_preco_criada"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('produto', 'tabela_preco', 'data_inicial')
        ordering = ['-data_inicial']

    def __str__(self):
        return f'{self.produto} - {self.tabela_preco} ({self.data_inicial})'
