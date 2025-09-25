# suprimentos/services/estoque.py

from suprimentos.models.estoque_movimento import EstoqueMovimento
from suprimentos.models.estoque import Estoque
from decimal import Decimal

def gerar_movimentos_estoque(documento, tipo="E"):
    """
    Gera movimentos de estoque a partir de um documento.
    :param documento: objeto que contém os itens (nota de entrada, pedido de venda, etc.)
    :param tipo: 'E' para entrada ou 'S' para saída
    """
    for item in documento.itens.all():
        # Consulta ou cria o saldo atual
        estoque, _ = Estoque.objects.get_or_create(
            produto=item.produto,
            deposito=item.deposito,
            defaults={'saldo': 0}
        )

        quantidade_anterior = estoque.saldo

        if tipo == "E":
            nova_quantidade = quantidade_anterior + Decimal(item.quantidade)
        elif tipo == "S":
            nova_quantidade = quantidade_anterior - Decimal(item.quantidade)
            if nova_quantidade < 0:
                raise ValueError(
                    f"Saldo insuficiente para o produto {item.produto}. "
                    f"Saldo atual: {quantidade_anterior}, solicitado: {item.quantidade}"
                )
        else:
            raise ValueError("Tipo inválido. Use 'E' para entrada ou 'S' para saída.")

        # Atualiza o saldo no estoque
        estoque.saldo = nova_quantidade
        estoque.save()

        # Cria o movimento de estoque
        EstoqueMovimento.objects.create(
            produto=item.produto,
            deposito=item.deposito,
            tipo=tipo,
            quantidade=item.quantidade,
            quantidade_anterior=quantidade_anterior,
            quantidade_estoque=nova_quantidade,
            fornecedor=getattr(documento, "fornecedor", None) if tipo == "E" else None,
            numero_nota=getattr(documento, "numero", None) if tipo == "E" else "",
            serie_nota=getattr(documento, "serie", None) if tipo == "E" else "",
            cliente=getattr(documento, "cliente", None) if tipo == "S" else None,
            venda = documento if tipo == "S" else None
        )
