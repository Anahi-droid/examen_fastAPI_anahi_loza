# app/materias.py — primera parte
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.datos import SERVICIOS
from app.esquemas import Servicio, ServicioActualizar, ServicioCrear

router = APIRouter(prefix="/servicios", tags=["servicios"])


def obtener_servicio(codigo: str) -> dict:
    """Devuelve el diccionario de la materia o lanza 404."""
    for servicio in SERVICIOS:
        if servicio["codigo"] == codigo.upper():
            return servicio
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el servicio '{codigo}'",
    )


ServicioEncontrada = Annotated[dict, Depends(obtener_servicio)]

# app/materias.py — segunda parte: el CRUD


@router.get("", response_model=list[Servicio])
def listar_servicios(
    complejidad: Annotated[int | None, Query(ge=1, le=10)] = None,
    requiere_repuesto: bool = False,
) -> list[dict]:
    resultado = SERVICIOS
    if complejidad is not None:
        resultado = [m for m in resultado if m["complejidad"] == complejidad]
    if requiere_repuesto:
        resultado = [m for m in resultado if m["requiere_repuesto"]]
    return resultado


@router.post("", response_model=Servicio, status_code=status.HTTP_201_CREATED)
def crear_servicio(nueva: ServicioCrear) -> dict:
    if any(m["codigo"] == nueva.codigo for m in SERVICIOS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El servicio '{nueva.codigo}' ya existe",
        )
    SERVICIOS.append(nueva.model_dump())
    return SERVICIOS[-1]


@router.get("/{codigo}", response_model=Servicio)
def ver_servicio(servicio: ServicioEncontrada) -> dict:
    return servicio


@router.put("/{codigo}", response_model=Servicio)
def actualizar_servicio(cambios: ServicioActualizar, servicio: ServicioEncontrada) -> dict:
    servicio.update(cambios.model_dump(exclude_unset=True))
    return servicio


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(servicio: ServicioEncontrada) -> None:
    SERVICIOS.remove(servicio)