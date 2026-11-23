# app/esquemas.py
from pydantic import BaseModel, Field


class ServicioBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    costo: int = Field(ge=1, le=500)
    complejidad: int = Field(ge=1, le=10)
    requiere_repuesto: bool = True


class ServicioCrear(ServicioBase):
    # Tres letras mayúsculas + tres dígitos: MAT101, PRG201...
    codigo: str = Field(pattern=r"^[A-Z]{3}\d{3}$")


class ServicioActualizar(BaseModel):
    # Todos opcionales: en un PUT parcial, lo que no se envía no se toca.
    nombre: str | None = Field(default=None, min_length=3, max_length=100)
    costo: int | None = Field(default=None, ge=1, le=500)
    complejidad: int | None = Field(default=None, ge=1, le=10)
    requiere_repuesto: bool | None = None


class Servicio(ServicioCrear):
    """Lo que la API devuelve: los cinco campos completos."""