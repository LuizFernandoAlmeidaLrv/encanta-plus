from django.db import models
from django.utils.timezone import now



# Modelo para FamiliaProduto
class FamiliaProduto(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

# Modelo para Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50) 
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    familia = models.ForeignKey(FamiliaProduto, on_delete=models.CASCADE, null=True, blank=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)  # Campo de imagem

    def __str__(self):
        return f"{self.nome} - {self.familia.nome} - R$ {self.preco:.2f}"


# Modelo para Forma de Pagamento
class FormaPagamento(models.Model):
    TIPO_CHOICES = [
        ('V', 'Voucher'),
        ('H', 'Cheque'),
        ('R', 'Cartão'),
        ('C', 'Crediário'),
        ('D', 'Dinheiro'),
        ('S', 'Voucher (Sinistro)'),
        ('I', 'Ifood (Semanal)'),
        ('P', 'Pix'),
    ] 
    id_forma_pagamento = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50)
    prazo_vencimento = models.IntegerField(default=0)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return self.descricao


# Modelo para Lista
class Lista(models.Model):
    id = models.AutoField(primary_key=True)  # ID_LISTA (PK)
    descricao = models.CharField(max_length=255, unique=True)  # Nome da lista
    lista = models.CharField(max_length=100)  # Nome interno ou código da lista

    def __str__(self):
        return f"{self.lista} - {self.descricao}"

# Modelo para ListaItem
class ListaItem(models.Model):
    descricao = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField(blank=True, null=True)  # Ordem será gerada automaticamente
    valor = models.CharField(max_length=100)
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name="itens")

    def save(self, *args, **kwargs):
        if self.ordem is None:
            ultimo_item = ListaItem.objects.filter(lista=self.lista).order_by('-ordem').first()
            self.ordem = (ultimo_item.ordem + 1) if ultimo_item else 1  # Incrementa baseado no último item
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lista.descricao} - {self.descricao} ({self.ordem})"


