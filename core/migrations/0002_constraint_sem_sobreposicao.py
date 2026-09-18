from django.db import migrations


class Migration(migrations.Migration):
    """Impede no BANCO que duas reservas do mesmo recurso se sobreponham.

    btree_gist permite misturar comparacao de igualdade (recurso_id) com
    comparacao de sobreposicao de intervalo (&&) no mesmo indice GiST.
    """

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS btree_gist;",
            reverse_sql="DROP EXTENSION IF EXISTS btree_gist;",
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE core_reserva
                ADD CONSTRAINT sem_sobreposicao
                EXCLUDE USING gist (
                    recurso_id WITH =,
                    tstzrange(inicio, fim) WITH &&
                );
            """,
            reverse_sql="""
                ALTER TABLE core_reserva
                DROP CONSTRAINT IF EXISTS sem_sobreposicao;
            """,
        ),
    ]
