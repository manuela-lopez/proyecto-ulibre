# Documentacion del Proyecto

## Arquitectura

El proyecto usa Python con tres piezas principales:

- FastAPI expone una API para consultar medicamentos.
- SQLite guarda los datos normalizados de INVIMA y la informacion curada.
- Telegram consume la misma logica de busqueda para responder al usuario.

## Flujo de datos

1. `scripts/load_medicines.py` consulta el dataset `i7cb-raxc` de Datos Abiertos Colombia.
2. Los campos oficiales se normalizan a nombres internos.
3. La informacion se guarda en `data/medicamentos.db`.
4. La busqueda usa coincidencia aproximada con RapidFuzz.
5. El bot responde con estado, registro, informacion curada y advertencia medica.

## Ejecucion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m scripts.load_medicines --limit 5000
uvicorn app.main:app --reload
python -m bot.telegram_bot
```
