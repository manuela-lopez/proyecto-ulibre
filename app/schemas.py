from datetime import date

from pydantic import BaseModel


class MedicamentoOut(BaseModel):
    id: int
    nombre_medicamento: str
    principio_activo: str | None = None
    registro_invima: str | None = None
    estado_registro: str | None = None
    fecha_vencimiento: date | None = None
    titular: str | None = None
    descripcion_comercial: str | None = None
    fuente: str
    para_que_sirve: str | None = None
    efectos_secundarios: str | None = None
    score: float | None = None

    model_config = {"from_attributes": True}


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[MedicamentoOut]
