from concurrent.futures import ThreadPoolExecutor

import pytest
import requests

from core.models import Recurso

TOTAL_REQUISICOES = 20


@pytest.mark.django_db(transaction=True)
def test_vinte_requisicoes_simultaneas_apenas_uma_grava(live_server):
    """20 pessoas tentam reservar o mesmo horario ao mesmo tempo."""

    recurso = Recurso.objects.create(nome="Sala A")

    payload = {
        "recurso": recurso.id,
        "cliente_nome": "Concorrente",
        "inicio": "2026-10-01T10:00:00-03:00",
        "fim": "2026-10-01T11:00:00-03:00",
    }

    def reservar(_):
        return requests.post(f"{live_server.url}/reservas", json=payload).status_code

    with ThreadPoolExecutor(max_workers=TOTAL_REQUISICOES) as executor:
        status_codes = list(executor.map(reservar, range(TOTAL_REQUISICOES)))

    criadas = status_codes.count(201)
    conflitos = status_codes.count(409)

    print(f"\nCriadas: {criadas} | Conflitos (409): {conflitos}")

    assert criadas == 1
    assert conflitos == TOTAL_REQUISICOES - 1