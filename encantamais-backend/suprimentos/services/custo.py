from produtos.models.produtocusto import ProdutoCusto
from produtos.models.produto import Produto

def criar_custo_automatico(item_nf, usuario):
    try:
        print("🔧 Iniciando criação de custo automático")
        print("📦 Dados recebidos:", item_nf)

        produto = Produto.objects.get(codigo=item_nf['produto'])

        ultima_sequencia = (
            ProdutoCusto.objects
            .filter(produto=produto)
            .order_by('-sequencia')
            .values_list('sequencia', flat=True)
            .first()
        )
        nova_sequencia = (ultima_sequencia or 0) + 1

        custo = ProdutoCusto.objects.create(
            produto=produto,
            data_custo=item_nf.get('data_custo'),
            sequencia=nova_sequencia,
            valor_base=item_nf.get('valor_base'),
            perc_frete=item_nf.get('perc_frete'),
            valor_frete=item_nf.get('valor_frete'),
            valor_custo=item_nf.get('valor_custo'),
            custo_medio=produto.custo_medio,
            tipo_custo='A',
            numero_nota=item_nf.get('numero_nota'),
            serie_nota=item_nf.get('serie_nota'),
            seq_item=item_nf.get('seq_item'),
            cod_fornecedor=item_nf.get('cod_fornecedor'),
            situacao='N',
            atualiza_custo_preco='S',
            usuario_gerador=usuario,
            data_geracao=item_nf.get('data_custo'),
            hora_geracao=int(item_nf.get('hora_custo') or 0)
        )

        print("✅ Custo criado com ID:", custo.produto)

    except Produto.DoesNotExist:
        print("❌ Produto não encontrado:", item_nf.get('produto'))

    except Exception as e:
        print("❌ Erro inesperado ao criar custo automático:", str(e))
