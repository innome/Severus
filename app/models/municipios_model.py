from pydantic import BaseModel


class MunicipioModel(BaseModel):
    codigo_municipio: str
    nombre: str
