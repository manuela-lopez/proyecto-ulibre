from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database import Base, get_engine
from app.models import Medicamento

SOURCE_NAME = "Datos Abiertos Colombia - INVIMA"

COLUMN_MAP = {
    "producto": "nombre_medicamento",
    "principioactivo": "principio_activo",
    "registrosanitario": "registro_invima",
    "estadoregistro": "estado_registro",
    "fechavencimiento": "fecha_vencimiento",
    "titular": "titular",
    "descripcioncomercial": "descripcion_comercial",
    "expediente": "expediente",
}


def fetch_records(limit: int, offset: int = 0) -> list[dict]:
    settings = get_settings()
    url = f"{settings.datos_gov_base_url}/{settings.datos_gov_dataset_id}.json"
    response = requests.get(url, params={"$limit": limit, "$offset": offset}, timeout=60)
    response.raise_for_status()
    return response.json()


def normalize_records(records: list[dict]) -> pd.DataFrame:
    rows = []
    for record in records:
        row = {target: record.get(source) for source, target in COLUMN_MAP.items()}
        row["fuente"] = SOURCE_NAME
        rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["nombre_medicamento"] = df["nombre_medicamento"].fillna("").str.strip()
    df = df[df["nombre_medicamento"] != ""].copy()
    df["fecha_vencimiento"] = pd.to_datetime(df["fecha_vencimiento"], errors="coerce").dt.date
    return df.drop_duplicates(subset=["nombre_medicamento", "registro_invima", "expediente"])


def load_to_sqlite(df: pd.DataFrame, database_url: str) -> int:
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    normalized_df = df.astype(object).where(pd.notnull(df), None)
    records = normalized_df.to_dict(orient="records")
    with Session() as session:
        session.execute(delete(Medicamento))
        session.add_all(Medicamento(**record) for record in records)
        session.commit()
    return len(df)


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga medicamentos INVIMA desde Datos Abiertos.")
    parser.add_argument("--limit", type=int, default=5000)
    parser.add_argument("--database-url", default=get_settings().database_url)
    args = parser.parse_args()

    Path("data").mkdir(exist_ok=True)
    records = fetch_records(limit=args.limit)
    df = normalize_records(records)
    total = load_to_sqlite(df, args.database_url)
    print(f"{datetime.now().isoformat(timespec='seconds')} - cargados {total} medicamentos")


if __name__ == "__main__":
    main()
