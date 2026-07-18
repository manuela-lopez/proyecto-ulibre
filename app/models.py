from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_medicamento: Mapped[str] = mapped_column(String(300), index=True)
    principio_activo: Mapped[str | None] = mapped_column(String(300), index=True)
    registro_invima: Mapped[str | None] = mapped_column(String(120), index=True)
    estado_registro: Mapped[str | None] = mapped_column(String(120), index=True)
    fecha_vencimiento: Mapped[Date | None] = mapped_column(Date, nullable=True)
    titular: Mapped[str | None] = mapped_column(String(300), nullable=True)
    descripcion_comercial: Mapped[str | None] = mapped_column(Text, nullable=True)
    expediente: Mapped[str | None] = mapped_column(String(120), nullable=True)
    fuente: Mapped[str] = mapped_column(String(300), default="Datos Abiertos Colombia - INVIMA")
