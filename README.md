# Rinha de Backend - 2024/Q1

## Descrição

A Rinha de Backend é um desafio que tem como principal objetivo compartilhar conhecimento em formato de desafio! Esta é a segunda edição. A data limite para enviar sua submissão é 10 de Março de 2024 às 23:59:59 e em 14 de Março de 2024 às 19:00 os resultados serão anunciados numa live no YouTube.

## Funcionalidades

A API oferece os seguintes endpoints:

### Transações

- **Requisição**

  `POST /clientes/[id]/transacoes`

  ```json
  {
    "valor": 1000,
    "tipo": "c",
    "descricao": "descricao"
  }
  ```

- **Resposta**
- HTTP Status: 201

  ```json
  {
    "limite": 100000,
    "saldo": -9098
  }
  ```

### Extrato

- **Requisição**

  `GET /clientes/[id]/extrato`

- **Resposta**
- HTTP Status: 200

  ```json
  {
    "saldo": {
      "total": -9098,
      "data_extrato": "2024-01-17T02:34:41.217753Z",
      "limite": 100000
    },
    "ultimas_transacoes": [
      {
        "valor": 10,
        "tipo": "c",
        "descricao": "descricao",
        "realizada_em": "2024-01-17T02:34:38.543030Z"
      },
      {
        "valor": 90000,
        "tipo": "d",
        "descricao": "descricao",
        "realizada_em": "2024-01-17T02:34:38.543030Z"
      }
    ]
  }
  ```

### Tecnologias

- **Linguagem de Programação**: Python
- **Banco de Dados**: PostgreSQL
- **Cliente Banco de Dados**: asyncpg

### Benchmarks Frameworks

| Name | Total Requests | Successful Requests | Failed Requests |  Min Response Time (ms) | Max Response Time (ms) | Mean Response Time (ms) | Std Deviation (ms) | 50th Percentile (ms) | 75th Percentile (ms) | 95th Percentile (ms) | 99th Percentile (ms) | Mean Requests Per Second | Successful Requests Per Second | Failed Requests Per Second |
| --------------- | --------------- | ------------------- | --------------- | ----- | ---- | ----- | -------------- | ---------------- | ---------------- | ---------------- | ---------------- | ------------------------- | ------------------------------ | -------------------------- |
| Starlette | 123243 | 123243 | 0 | 0 | 75 | 2 | 2 | 1 | 2 | 3 | 10 | 503.03 | 503.03 | 0 |
| Fastapi | 123243 | 98769 | 24474 | 0 | 6591 | 277 | 562 | 2 | 69 | 1074 | 2698 | 500.99 | 401.5 | 99.49 |
| Uvicorn | 123243 | 123243 | 0 | 0 | 83 | 2 | 2 | 1 | 2 | 2 | 5 | 503.03 | 503.03 | 0 |
| Robyn | 123243 | 123243 | 0 | 0 | 77 | 1 | 2 | 1 | 2 | 2 | 4 | 503.03 | 503.03 | 0 |
