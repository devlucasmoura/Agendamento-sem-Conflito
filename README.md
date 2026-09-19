# Agendamento sem Conflito

API REST que garante que **duas reservas do mesmo recurso nunca se sobreponham**,
mesmo sob requisicoes simultaneas.

## O problema

Sistemas de agendamento ingenuos fazem:

```python
if not Reserva.objects.filter(...).exists():
    Reserva.objects.create(...)
```

Entre o `if` e o `create` existe uma janela. Duas requisicoes simultaneas passam
pelo `if` ao mesmo tempo e ambas gravam. E a classica *race condition*.

## A solucao: duas camadas

1. **Aplicacao** — `transaction.atomic()` + `select_for_update()` no recurso.
   Requisicoes para o mesmo recurso passam a ser enfileiradas: a segunda espera
   a primeira terminar e ja enxerga a reserva gravada.
2. **Banco** — constraint `EXCLUDE USING gist` no PostgreSQL. Mesmo que o codigo
   tenha bug ou alguem insira direto no banco, a sobreposicao e impossivel.

A camada 1 da a mensagem de erro limpa (`409 Conflict`). A camada 2 e a rede de
seguranca.

## Stack

Python 3.12 · Django 5 + DRF · PostgreSQL 16 · Docker Compose · pytest

## Como rodar

```bash
cp .env.example .env
docker compose up --build
docker compose exec api python manage.py migrate
```

API em `http://localhost:8000`.

## Endpoints

| Metodo | Rota | Retorno |
|---|---|---|
| POST | `/recursos` | 201 |
| GET | `/recursos` | 200 |
| POST | `/reservas` | 201, 400 (datas invalidas), **409 (conflito)** |
| GET | `/reservas` | 200 |
| DELETE | `/reservas/{id}` | 204 |

## Testes

```bash
docker compose exec api pytest -v
```

Inclui teste de concorrencia: 20 threads disparam a mesma reserva
simultaneamente; exatamente 1 grava e 19 recebem 409.

## Conflito barrado na prática

![Requisição sobreposta recebendo 409](docs/erro409.png)

Reserva das 10h às 11h já existente; nova tentativa no mesmo horário recebe
409 do banco, não de um `if` no código.

## Proximos passos

- Endpoint de disponibilidade (`GET /recursos/{id}/disponibilidade?data=`)
- Autenticacao por token
- Cancelamento com regra de antecedencia minima
