import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recurso",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=120)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Reserva",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cliente_nome", models.CharField(max_length=120)),
                ("inicio", models.DateTimeField()),
                ("fim", models.DateTimeField()),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                (
                    "recurso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservas",
                        to="core.recurso",
                    ),
                ),
            ],
            options={"ordering": ["inicio"]},
        ),
    ]
