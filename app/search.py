from rapidfuzz import fuzz, process
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.clinical_info import load_clinical_info, normalize_text
from app.config import get_settings
from app.models import Medicamento
from app.schemas import MedicamentoOut


def _search_text(medicine: Medicamento) -> str:
    return normalize_text(
        " ".join(
            value
            for value in [
                medicine.nombre_medicamento,
                medicine.principio_activo,
                medicine.descripcion_comercial,
                medicine.registro_invima,
            ]
            if value
        )
    )


def search_medicines(db: Session, query: str, limit: int = 5) -> list[MedicamentoOut]:
    normalized_query = normalize_text(query)
    if not normalized_query:
        return []

    medicines = db.scalars(select(Medicamento)).all()
    choices = {medicine.id: _search_text(medicine) for medicine in medicines}
    matches = process.extract(
        normalized_query,
        choices,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=55,
    )
    by_id = {medicine.id: medicine for medicine in medicines}
    clinical = load_clinical_info(get_settings().clinical_info_path)

    results: list[MedicamentoOut] = []
    for _, score, medicine_id in matches:
        medicine = by_id[medicine_id]
        info = (
            clinical.get(normalize_text(medicine.nombre_medicamento))
            or clinical.get(normalize_text(medicine.principio_activo))
            or {}
        )
        item = MedicamentoOut.model_validate(medicine)
        item.score = float(score)
        item.para_que_sirve = info.get("para_que_sirve") or None
        item.efectos_secundarios = info.get("efectos_secundarios") or None
        results.append(item)
    return results
