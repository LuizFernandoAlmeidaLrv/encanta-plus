from datetime import date
from .models import TabelaPreco, TabelaPrecoProduto

def get_preco_para_venda(produto):
    hoje = date.today()

    tabelas_ativas = TabelaPreco.objects.filter(
        ativa=True,
        data_inicio__lte=hoje
    ).filter(
        models.Q(data_fim__isnull=True) | models.Q(data_fim__gte=hoje)
    ).order_by('prioridade', '-data_inicio')

    for tabela in tabelas_ativas:
        item = produto.tabela_precos.filter(tabela=tabela, ativo=True).first()
        if item:
            return item.preco

    return None  # Nenhum preço encontrado
