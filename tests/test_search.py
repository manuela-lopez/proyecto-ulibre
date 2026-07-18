from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Medicamento
from app.search import search_medicines


def test_search_finds_approximate_match():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    with Session() as db:
        db.add(
            Medicamento(
                nombre_medicamento="ACETAMINOFEN 500 MG TABLETA",
                principio_activo="Acetaminofen",
                registro_invima="INVIMA 2020M-000000",
                estado_registro="Vigente",
                fecha_vencimiento=date(2030, 1, 1),
                titular="Titular de prueba",
                descripcion_comercial="Analgesico",
                fuente="Prueba",
            )
        )
        db.commit()

        results = search_medicines(db, "acetaminofen")

    assert len(results) == 1
    assert results[0].registro_invima == "INVIMA 2020M-000000"
    assert results[0].estado_registro == "Vigente"
