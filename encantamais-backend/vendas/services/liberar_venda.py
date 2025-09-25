def verificar_liberacao(venda):
    titulo = venda.titulo

    if venda.tipo == 'AV':
        return titulo.situacao == 'R'
    elif venda.tipo == 'AP':
        return titulo.data_recebimento is not None or not tem_entrada(venda)
    return False

def tem_entrada(venda):
    # Implementar se houver controle de entrada parcelada
    return False
