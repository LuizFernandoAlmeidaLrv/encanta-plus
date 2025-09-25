from rest_framework import serializers
from datetime import datetime
from datetime import date
from cadastro.models import ListaItem
from django.utils.timezone import now
from pedido.models import Pedido, PedidoItem, PedidoItemComposicao, Composicao
from cadastro.models import Cardapio, CardapioIngredientes, Ingrediente, Produto, FormaPagamento, Cliente, ListaItem
from cadastro.serializers import CardapioIngredientesSerializer, ListaItemSerializer 

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone']  # Adapte conforme o que você precisa

# Serializer para a Situação do Pedido
class SituacaoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaItem
        fields = ['descricao']  # A descrição da situação

class ComposicaoSerializer(serializers.ModelSerializer):
    ingrediente = serializers.StringRelatedField()  # ou um serializer do ingrediente
    class Meta:
        model = Composicao
        fields = ['ingrediente', 'quantidade']

# serializers.py


class PedidoItemComposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItemComposicao
        fields = ['ingrediente', 'quantidade']  # 🔄 Alterado de item_cardapio para ingrediente


class PedidoItemSerializer(serializers.ModelSerializer):
    pedido = serializers.PrimaryKeyRelatedField(queryset=Pedido.objects.all())  # A chave primária do pedido
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())  # Pegamos o produto apenas pelo ID
    composicao = PedidoItemComposicaoSerializer(many=True, required=False)  # Composição de Ingredientes

    class Meta:
        model = PedidoItem
        fields = ['pedido', 'produto', 'quantidade_pedida', 'valor_unitario', 'composicao']

    def create(self, validated_data):
        composicao_data = validated_data.pop('composicao', [])  # Retira a composição dos dados validados

        # Criando o PedidoItem
        pedido_item = PedidoItem.objects.create(**validated_data)

        # Agora vamos salvar a composição, se houver dados de composição
        for comp_data in composicao_data:
            PedidoItemComposicao.objects.create(pedido_item=pedido_item, **comp_data)

        return pedido_item
class PedidoSerializer2(serializers.ModelSerializer):
    id_forma_pagamento = serializers.PrimaryKeyRelatedField(
        queryset=FormaPagamento.objects.all(),
        source="forma_de_pagamento"
    )
    tipo_entrega = serializers.IntegerField()
    itens = serializers.ListField(child=serializers.DictField(), write_only=True)  # Apenas para entrada de dados
    total = serializers.SerializerMethodField()
    situacao_do_pedido = serializers.CharField() 
    class Meta:
        model = Pedido
        fields = [
            "numero_pedido",
            "cliente", 
            "id_forma_pagamento",
            "tipo_entrega", 
            "situacao_do_pedido",
            "valor_pedido",
            "itens",  # Apenas para entrada de dados
            "total"
        ]

    def get_total(self, obj):
        return sum(item.valor_unitario * item.quantidade_pedida for item in obj.itens.all())

    def create(self, validated_data):
        """
        Apenas cria o pedido e retorna, sem inserir os itens.
        A criação dos itens será feita na View.
        """
        validated_data.pop('itens', None)  # Remove os itens para evitar erro
        pedido = Pedido.objects.create(**validated_data)
        return pedido

class PedidoSerializer(serializers.ModelSerializer):
    id_forma_pagamento = serializers.PrimaryKeyRelatedField(
        queryset=FormaPagamento.objects.all(),
        source="forma_de_pagamento"
    )
    tipo_entrega = serializers.IntegerField()
    itens = serializers.ListField(child=serializers.DictField(), write_only=True)  # Apenas para entrada de dados
    total = serializers.SerializerMethodField()
    cliente = ClienteSerializer()  # Altere para receber apenas o ID do cliente
    situacao_do_pedido =  serializers.StringRelatedField() # Alterado para o ID da situação

    class Meta:
        model = Pedido
        fields = [
            "numero_pedido",
            "cliente", 
            "id_forma_pagamento",
            "tipo_entrega", 
            "situacao_do_pedido",
            "valor_pedido",
            "itens",  # Apenas para entrada de dados
            "total"
        ]

    def get_total(self, obj):
        return sum(item.valor_unitario * item.quantidade_pedida for item in obj.itens.all())

    def create(self, validated_data):
        """
        Apenas cria o pedido e retorna, sem inserir os itens.
        A criação dos itens será feita na View.
        """
        validated_data.pop('itens', None)  # Remove os itens para evitar erro
        pedido = Pedido.objects.create(**validated_data)
        return pedido


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nome', 'descricao']

class CardapioIngredientesSerializer(serializers.ModelSerializer):
    ingrediente = IngredienteSerializer()

    class Meta:
        model = CardapioIngredientes
        fields = ['cardapio', 'ingrediente']


class ProdutoSerializer(serializers.ModelSerializer):
    ingredientes = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'tipo', 'preco', 'ingredientes', 'familia', 'imagem']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_ingredientes(self, obj):       

        if str(obj.tipo) != "2":
           
            return []
        # Mapeamento de número -> nome do dia (igual ao banco)
        dias_semana = {
        0: "segunda",
        1: "terca",
        2: "quarta",
        3: "quinta",
        4: "sexta",
        5: "sabado",
        6: "domingo",
        }
        dia_da_semana = date.today().weekday()
       # Obtém o nome do dia correspondente ao número atual
        dia_hoje = dias_semana[date.today().weekday()]
        
        # Busca o cardápio do dia no banco
        cardapio = Cardapio.objects.filter(dia_da_semana=dia_hoje).first()

        if not cardapio:
            return []

        ingredientes = CardapioIngredientes.objects.filter(cardapio=cardapio).select_related('ingrediente')

        ingredientes_lista = [
            {"ingrediente": ingrediente.ingrediente.id , "nome":  ingrediente.ingrediente.nome, "quantidade": ingrediente.quantidade}
                for ingrediente in ingredientes
        ]
       
        print("\n🔹 imprimirIngrediente...", ingredientes_lista)
        return ingredientes_lista



