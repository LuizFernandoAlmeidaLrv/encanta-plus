from django.db import models
from django.contrib.auth.models import User

class CaixasVale(models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    situacao = models.CharField(
        max_length=1,
        choices=[("A", "Aberto"), ("B", "Baixado")],
        default="A"
    )

    def __str__(self):
        return f"Vale {self.id} - R$ {self.valor} - {self.get_situacao_display()}"
