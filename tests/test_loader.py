from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import Medicamento
from scripts.load_medicines import load_to_sqlite, normalize_records


def test_loader_normalizes_and_persists_records(tmp_path):
    records = [
        {
            "producto": " ACETAMINOFEN 500 MG ",
            "principioactivo": "Acetaminofen",
            "registrosanitario": "INVIMA 2020M",
            "estadoregistro": "Vigente",
            "fechavencimiento": "2030-01-01T00:00:00.000",
            "titular": "Titular",
            "descripcioncomercial": "Tableta",
            "expediente": "123",
        },
        {
            "producto": "IBUPROFENO 400 MG",
            "principioactivo": "Ibuprofeno",
            "registrosanitario": "INVIMA 2021M",
            "estadoregistro": "Vigente",
            "titular": "Titular",
            "descripcioncomercial": "Tableta",
            "expediente": "456",
        }
    ]
    df = normalize_records(records)
    database_url = f"sqlite:///{tmp_path / 'medicamentos.db'}"

    total = load_to_sqlite(df, database_url)

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        stored = session.scalars(select(Medicamento).order_by(Medicamento.nombre_medicamento)).all()

    assert total == 2
    assert list(df["nombre_medicamento"]) == ["ACETAMINOFEN 500 MG", "IBUPROFENO 400 MG"]
    assert stored[0].registro_invima == "INVIMA 2020M"
    assert stored[1].fecha_vencimiento is None
