from config.database import get_collection
from typing import List
from models.municipios_model import MunicipioModel
import unicodedata

async def obtener_todos_los_municipios(skip: int = 0) -> List[MunicipioModel]:
    """Obtiene todos los municipios con paginación."""
    collection = get_collection("municipios")
    cursor = collection.find().skip(skip)
    return [MunicipioModel(**doc) async for doc in cursor]


async def buscar_municipio_por_codigo(codigo_municipio: str) -> MunicipioModel:
    """Busca un municipio por su código."""
    collection = get_collection("municipios")
    doc = await collection.find_one({"codigo_municipio": codigo_municipio})
    if not doc:
        return None
    return MunicipioModel(**doc)


def eliminar_diacriticos(texto: str) -> str:
    """
    Elimina diacríticos (tildes) de una cadena.
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )

async def buscar_municipios_por_nombre(nombre: str) -> List[MunicipioModel]:
    """
    Busca municipios cuyo nombre contenga el valor proporcionado,
    comparando contra el campo `nombre_normalizado`.
    """
    collection = get_collection("municipios")
    nombre_normalizado = eliminar_diacriticos(nombre)

    cursor = collection.find(
        {"nombre_normalizado": {"$regex": f"{nombre_normalizado}", "$options": "i"}}
    )
    return [MunicipioModel(**doc) async for doc in cursor]