from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from models.municipios_model import MunicipioModel
from services.municipios_service import obtener_todos_los_municipios, buscar_municipio_por_codigo, buscar_municipios_por_nombre
from config.auth import get_current_user

router = APIRouter(prefix="/municipios", tags=["Municipios"])


@router.get("/", response_model=List[MunicipioModel], dependencies=[Depends(get_current_user)])
async def listar_municipios(skip: int = Query(0)):
    """
    Lista todos los municipios con soporte de paginación.
    - `skip`: número de registros a omitir.
    - `limit`: número máximo de registros a devolver.
    """
    municipios = await obtener_todos_los_municipios(skip)
    return municipios


@router.get("/{codigo_municipio}", response_model=MunicipioModel, dependencies=[Depends(get_current_user)])
async def obtener_municipio(codigo_municipio: str):
    """
    Obtiene un municipio por su código.
    - `codigo_municipio`: código del municipio a buscar.
    """
    municipio = await buscar_municipio_por_codigo(codigo_municipio)
    if not municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return municipio

@router.get("/buscar/", response_model=List[MunicipioModel], dependencies=[Depends(get_current_user)])
async def buscar_municipios(nombre: str):
    """
    Busca municipios por nombre, insensible a tildes y mayúsculas/minúsculas.
    - `nombre`: Parte del nombre del municipio a buscar.
    """
    municipios = await buscar_municipios_por_nombre(nombre)
    if not municipios:
        raise HTTPException(status_code=404, detail="No se encontraron municipios con ese nombre")
    return municipios