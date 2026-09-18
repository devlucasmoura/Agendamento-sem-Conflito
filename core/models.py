from django.db import models


class Recurso(models.Model):
    """Aquilo que se reserva: uma sala, um medico, uma quadra."""

    nome = models.CharField(max_length=120)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    recurso = models.ForeignKey(
        Recurso, on_delete=models.CASCADE, related_name="reservas"
    )
    cliente_nome = models.CharField(max_length=120)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["inicio"]

    def __str__(self):
        return f"{self.recurso} {self.inicio:%d/%m %H:%M}-{self.fim:%H:%M}"
