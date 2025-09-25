from rest_framework import serializers
from decimal import Decimal
from suprimentos.models.nota_fiscal_entrada import NotaFiscalEntrada
from suprimentos.models.nota_item_entrada import NotaFiscalEntradaItem
from suprimentos.serializers.nota_fiscal_entrada_item_serializer import NotaFiscalEntradaItemSerializer
from suprimentos.services.estoque import gerar_movimentos_estoque

class NotaFiscalEntradaSerializer(serializers.ModelSerializer):
    itens = NotaFiscalEntradaItemSerializer(many=True)

    class Meta:
        model = NotaFiscalEntrada
        fields = [
            'id', 'numero', 'serie', 'fornecedor', 'data_emissao', 'data_entrada',
            'valor_total', 'valor_frete', 'observacao', 'situacao', 'itens'
        ]

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        nota = NotaFiscalEntrada.objects.create(**validated_data)

        for item_data in itens_data:
            quantidade = Decimal(item_data['quantidade'])
            valor_unitario = Decimal(item_data['valor_unitario'])
            percentual_frete = Decimal(item_data.get('percentual_frete', 0))

            valor_total = quantidade * valor_unitario
            valor_frete_aplicado = valor_total * (percentual_frete / 100)
            custo_unitario = (valor_total + valor_frete_aplicado) / quantidade

            NotaFiscalEntradaItem.objects.create(
                nota_fiscal=nota,
                produto=item_data['produto'],
                deposito=item_data['deposito'],
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total,
                percentual_frete=percentual_frete,
                valor_frete_aplicado=valor_frete_aplicado,
                custo_unitario_calculado=custo_unitario,
                aplicar_custo=False
            )

        # Somente gera movimento se a nota já estiver sendo criada como fechada
        if nota.situacao == '2':
            gerar_movimentos_estoque(nota)

        return nota

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Remove itens antigos
        instance.itens.all().delete()

        # Cria os novos itens com cálculo automático
        for item_data in itens_data:
            quantidade = Decimal(item_data['quantidade'])
            valor_unitario = Decimal(item_data['valor_unitario'])
            percentual_frete = Decimal(item_data.get('percentual_frete', 0))

            valor_total = quantidade * valor_unitario
            valor_frete_aplicado = valor_total * (percentual_frete / 100)
            custo_unitario = (valor_total + valor_frete_aplicado) / quantidade

            NotaFiscalEntradaItem.objects.create(
                nota_fiscal=instance,
                produto=item_data['produto'],
                deposito=item_data['deposito'],
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total,
                percentual_frete=percentual_frete,
                valor_frete_aplicado=valor_frete_aplicado,
                custo_unitario_calculado=custo_unitario,
                aplicar_custo=item_data.get('aplicar_custo', False)
            )

        return instance
