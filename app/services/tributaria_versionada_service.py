from bson.objectid import ObjectId
from typing import List, Optional
from config.database import get_collection
from models.tributaria_versionada_model import InformacionTributariaVersionadaModel

COLLECTION_NAME = "informacion_tributaria_versionada"

async def crear_informacion_tributaria_versionada(data: InformacionTributariaVersionadaModel) -> str:
    """
    Inserta un nuevo documento en la colección, representando 
    la información tributaria de un municipio con cierta versión.
    """
    collection = get_collection(COLLECTION_NAME)

    # Verificamos si existe ya (codigo_municipio, version)
    existente = await collection.find_one({
        "codigo_municipio": data.codigo_municipio,
        "version": data.version
    })
    if existente:
        raise ValueError("Ya existe un registro con este municipio y versión.")

    # Excluimos 'id' si viene en data para que Mongo genere uno nuevo
    dict_to_insert = data.dict(exclude={"id"})
    result = await collection.insert_one(dict_to_insert)
    return str(result.inserted_id)


async def obtener_informacion_tributaria_versionada_por_id(doc_id: str) -> Optional[InformacionTributariaVersionadaModel]:
    """
    Recupera un documento por _id de MongoDB.
    """
    collection = get_collection(COLLECTION_NAME)
    doc = await collection.find_one({"_id": ObjectId(doc_id)})
    if doc:
        return InformacionTributariaVersionadaModel(**doc)
    return None


async def obtener_informacion_tributaria_versionada_por_municipio_version(
    municipio_id: str, version: str
) -> Optional[InformacionTributariaVersionadaModel]:
    """
    Recupera un documento que coincida con (codigo_municipio, version).
    """
    collection = get_collection(COLLECTION_NAME)
    doc = await collection.find_one({
        "codigo_municipio": municipio_id,
        "version": version
    })
    if doc:
        return InformacionTributariaVersionadaModel(**doc)
    return None


async def listar_informacion_tributaria_versionada(skip: int = 0) -> List[InformacionTributariaVersionadaModel]:
    collection = get_collection(COLLECTION_NAME)
    cursor = collection.find({"activo": True}).skip(skip)
    results = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        results.append(InformacionTributariaVersionadaModel(**doc))
    return results


async def obtener_informacion_tributaria_versionada_por_municipio_version(
    municipio_id: str, 
    version: str
) -> Optional[InformacionTributariaVersionadaModel]:
    collection = get_collection("informacion_tributaria_versionada")
    doc = await collection.find_one({
        "codigo_municipio": municipio_id,
        "version": version
    })
    if doc:
        # Convertir _id en string y asignarlo al campo id
        doc["id"] = str(doc["_id"])
        return InformacionTributariaVersionadaModel(**doc)
    return None


async def deshabilitar_informacion_tributaria_por_municipio_version(municipio_id: str, version: str) -> bool:
    """
    Pone 'activo=false' en el documento que coincida con (municipio_id, version).
    Retorna True si la operación modificó el documento, False en caso contrario.
    """
    collection = get_collection("informacion_tributaria_versionada")
    result = await collection.update_one(
        {
            "codigo_municipio": municipio_id,
            "version": version,
            "activo": True  # Opcional, si quieres asegurarte de no reactivar algo ya inactivo
        },
        {"$set": {"activo": False}}
    )
    return result.modified_count > 0


async def actualizar_informacion_tributaria_versionada(doc_id: str, update_data: dict) -> bool:
    """
    Recibe un dict con los campos a actualizar y hace un $set en Mongo.
    """
    collection = get_collection(COLLECTION_NAME)
    result = await collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0