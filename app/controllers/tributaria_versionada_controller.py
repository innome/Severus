from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from models.tributaria_versionada_model import InformacionTributariaVersionadaModel
from models.informacion_tributaria_versionada_update_model import InformacionTributariaVersionadaUpdateModel
from services.tributaria_versionada_service import (
    crear_informacion_tributaria_versionada,
    obtener_informacion_tributaria_versionada_por_id,
    obtener_informacion_tributaria_versionada_por_municipio_version,
    listar_informacion_tributaria_versionada,
    actualizar_informacion_tributaria_versionada,
    deshabilitar_informacion_tributaria_por_municipio_version
)

router = APIRouter(prefix="/informacion_tributaria_versionada", tags=["Información Tributaria Versionada"])

@router.post("/", response_model=dict)
async def crear_informacion_versionada(data: InformacionTributariaVersionadaModel):
    """
    Crea un documento con toda la información tributaria de un municipio y su versión.
    """
    try:
        new_id = await crear_informacion_tributaria_versionada(data)
        return {"message": "Información creada con éxito", "id": new_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[InformacionTributariaVersionadaModel])
async def listar_informacion_versionada(skip: int = Query(0)):
    """
    Lista toda la información, paginada.
    """
    return await listar_informacion_tributaria_versionada(skip)

@router.get("/{municipio_id}/{version}", response_model=InformacionTributariaVersionadaModel)
async def obtener_informacion_por_municipio_version(municipio_id: str, version: str):
    """
    Obtiene la información del municipio y versión especificados.
    """
    doc = await obtener_informacion_tributaria_versionada_por_municipio_version(municipio_id, version)
    if not doc:
        raise HTTPException(status_code=404, detail="No se encontró información para ese municipio y versión.")
    return doc

@router.get("/por_id/{doc_id}", response_model=InformacionTributariaVersionadaModel)
async def obtener_informacion_por_id(doc_id: str):
    """
    Obtiene la información por _id de MongoDB.
    """
    doc = await obtener_informacion_tributaria_versionada_por_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="No se encontró información con ese ID.")
    return doc

@router.put("/{municipio_id}/{version}", response_model=dict)
async def actualizar_informacion_por_municipio_version(
    municipio_id: str,
    version: str,
    data: InformacionTributariaVersionadaUpdateModel
):
    """
    Actualiza parcialmente la información en base a (municipio_id, version).
    """
    # 1) Ubicar el doc existente
    doc_existente = await obtener_informacion_tributaria_versionada_por_municipio_version(municipio_id, version)
    if not doc_existente:
        raise HTTPException(status_code=404, detail="No se encontró el documento con esos datos.")

    # 2) Generar un dict solo con los campos enviados (exclude_unset=True se hace desde el modelo)
    update_data = data.dict(exclude_unset=True)

    # 3) Actualizar en base al _id del doc original
    actualizado = await actualizar_informacion_tributaria_versionada(doc_existente.id, update_data)
    if not actualizado:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el documento.")

    return {"message": "Información actualizada con éxito"}

@router.delete("/{municipio_id}/{version}", response_model=dict)
async def deshabilitar_por_municipio_version(municipio_id: str, version: str):
    """
    Soft-delete: marca 'activo=false' el documento que coincide con (municipio_id, version).
    """
    deshabilitado = await deshabilitar_informacion_tributaria_por_municipio_version(municipio_id, version)
    if not deshabilitado:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró documento activo para ese municipio y versión."
        )
    return {"message": "Información deshabilitada con éxito"}