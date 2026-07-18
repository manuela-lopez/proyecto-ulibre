from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Medicamento
from app.schemas import MedicamentoOut, SearchResponse
from app.search import search_medicines

app = FastAPI(title="Proyecto Ulibre Medicamentos API")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/medicamentos/buscar", response_model=SearchResponse)
def buscar_medicamentos(
    q: str = Query(min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
) -> SearchResponse:
    results = search_medicines(db, q, limit=limit)
    return SearchResponse(query=q, total=len(results), results=results)


@app.get("/medicamentos/{medicine_id}", response_model=MedicamentoOut)
def obtener_medicamento(medicine_id: int, db: Session = Depends(get_db)) -> MedicamentoOut:
    medicine = db.get(Medicamento, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return MedicamentoOut.model_validate(medicine)
