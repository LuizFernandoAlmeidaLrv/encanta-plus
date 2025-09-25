from django.db import models
SITUACAO = (
    ('A', 'Ativo'),
    ('I', 'Inativo'), 
)
SIM_NAO = (
    ('S', 'Sim'),
    ('N', 'Não'),
)

class FormaPagamento(models.Model):
    descricao = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=100, unique=True)
    permite_parcelas = models.CharField(max_length=1, choices=SIM_NAO, default='N')
    situacao = models.CharField(max_length=1, choices=SITUACAO, default='A')
   

    def __str__(self):
        return self.descricao
