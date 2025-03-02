from typing import Optional, List, Dict
from pydantic import BaseModel, RootModel

class Articulo(BaseModel):
    titulo: str = None
    contenido: str = None


class InfoExogenaMagnetica(BaseModel):
    titulo: Optional[str] = None
    ultimo_nit: Optional[List[int]] = None
    fecha_pago: Optional[str] = None
    fecha_vencimiento: Optional[str] = None
    contenido: Optional[str] = None

class FechaDict(RootModel[Dict[str, str]]):
    """
    Permite aceptar datos de la forma:
    {
      "0": "9 enero 2025"
    }
    sin campos adicionales.
    """
    pass

class InformacionTributariaVersionadaModel(BaseModel):
    """
    Un solo documento que contiene toda la información tributaria de un municipio
    con la posibilidad de diferentes versiones.
    """
    # Este 'id' se setea automáticamente por MongoDB, así que es opcional
    id: Optional[str] = None

    # Clave principal para agrupar la información
    codigo_municipio: str

    # Nuevo campo para manejar versiones
    version: str  # Ejemplo: "0.0.1"
    activo: bool = True

    url_pdf: Optional[str] = None
    calendario_tributario: Optional[str] = None

    estatuto_tributario: Optional[List[Articulo]] = None
    ica: Optional[List[Articulo]] = None
    autoretencion_ica: Optional[List[Articulo]] = None
    fechas_ica: Optional[List[FechaDict]] = None

    rete_ica: Optional[List[Articulo]] = None
    fechas_rete_ica: Optional[List[FechaDict]] = None

    impuesto_industria_comercio: Optional[str] = None

    periodicidad_impuestos: Optional[List[Dict[str, str]]] = None

    # Para almacenar medios magnéticos / información exógena
    informacion_exogena_municipal_medios_magneticos: Optional[List[InfoExogenaMagnetica]] = None
    vencimiento_declaraciones_x_nit: Optional[List[FechaDict]] = None
    vencimiento_declaraciones_x_nit_ica: Optional[List[FechaDict]] = None
    vencimiento_declaraciones_x_nit_rete_ica: Optional[List[FechaDict]] = None
