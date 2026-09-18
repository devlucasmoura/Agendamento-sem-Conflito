from django.db import IntegrityError, transaction
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Recurso, Reserva
from .serializers import RecursoSerializer, ReservaSerializer


class RecursoListCreate(generics.ListCreateAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer


class ReservaListCreate(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recurso_id = serializer.validated_data["recurso"].id

        try:
            with transaction.atomic():
                # Trava a linha do recurso: duas requisicoes para o mesmo
                # recurso passam a ser processadas uma de cada vez.
                Recurso.objects.select_for_update().get(pk=recurso_id)
                serializer.save()
        except IntegrityError:
            # A constraint EXCLUDE do Postgres barrou a sobreposicao.
            return Response(
                {"detail": "Horario ja reservado para este recurso."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservaDestroy(generics.DestroyAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
