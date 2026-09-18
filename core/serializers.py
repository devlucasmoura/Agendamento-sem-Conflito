from rest_framework import serializers

from .models import Recurso, Reserva


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ["id", "nome", "criado_em"]


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ["id", "recurso", "cliente_nome", "inicio", "fim", "criado_em"]

    def validate(self, dados):
        if dados["fim"] <= dados["inicio"]:
            raise serializers.ValidationError(
                {"fim": "O fim deve ser posterior ao inicio."}
            )
        return dados
