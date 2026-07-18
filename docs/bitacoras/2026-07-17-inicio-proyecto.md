# Bitacora - Inicio del Proyecto

Fecha: 2026-07-17

## Objetivo

Crear la base de un chatbot de Telegram para consultar informacion breve de medicamentos usando datos oficiales de INVIMA publicados en Datos Abiertos Colombia.

## Decisiones tecnicas

- Python como lenguaje principal.
- FastAPI para exponer consultas reutilizables.
- SQLite para el prototipo local.
- Telegram como primer canal.
- RapidFuzz para busqueda aproximada por nombre.
- Archivo curado local para usos y efectos secundarios principales.

## Fuente de datos

Dataset inicial: Codigo Unico de Medicamentos Vigentes, ID `i7cb-raxc`, Datos Abiertos Colombia/INVIMA.

## Limitaciones

El dataset oficial sirve para consultar registro, estado y datos administrativos. La informacion de uso y efectos secundarios se mantiene separada en una fuente curada local y debe revisarse antes de ampliar cobertura.

## Proximos pasos

- Validar columnas reales del dataset con una descarga de muestra.
- Cargar datos iniciales en SQLite.
- Probar busquedas con medicamentos frecuentes.
- Configurar token de Telegram para pruebas reales.
