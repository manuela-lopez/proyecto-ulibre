# Proyecto Ulibre

Base de un chatbot de Telegram para consultar informacion breve de medicamentos con datos oficiales de INVIMA publicados en Datos Abiertos Colombia.

## Stack

- Python
- FastAPI
- SQLite
- Pandas
- RapidFuzz
- Telegram Bot API

## Configuracion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configura `TELEGRAM_BOT_TOKEN` en `.env` para usar el bot.

## Cargar datos

```bash
python -m scripts.load_medicines --limit 5000
```

La fuente inicial es el dataset `i7cb-raxc` de Datos Abiertos Colombia/INVIMA.

## Ejecutar API

```bash
uvicorn app.main:app --reload
```

Endpoints principales:

- `GET /health`
- `GET /medicamentos/buscar?q=acetaminofen`
- `GET /medicamentos/{id}`

## Ejecutar bot de Telegram

```bash
python -m bot.telegram_bot
```

## Pruebas

```bash
pytest
```

La informacion de uso y efectos secundarios se maneja inicialmente en `data/info_clinica.csv`. La respuesta del bot siempre incluye una advertencia de que la informacion no reemplaza a un profesional de salud.
