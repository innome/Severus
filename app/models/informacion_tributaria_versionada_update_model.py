# models/informacion_tributaria_versionada_update_model.py

from typing import Optional, List, Dict
from pydantic import BaseModel, RootModel

class ArticuloUpdate(BaseModel):
    titulo: Optional[str] = None
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

class InfoExogenaMagneticaUpdate(BaseModel):
    titulo: Optional[str] = None
    ultimo_nit: Optional[List[int]] = None
    fecha_pago: Optional[str] = None
    fecha_vencimiento: Optional[str] = None
    contenido: Optional[str] = None

class InformacionTributariaVersionadaUpdateModel(BaseModel):
    # Todos los campos en modo opcional
    codigo_municipio: Optional[str] = None
    version: Optional[str] = None
    url_pdf: Optional[str] = None
    calendario_tributario: Optional[str] = None

    estatuto_tributario: Optional[List[ArticuloUpdate]] = None
    ica: Optional[List[ArticuloUpdate]] = None
    autoretencion_ica: Optional[List[ArticuloUpdate]] = None

    informacion_exogena_municipal_medios_magneticos: Optional[List[InfoExogenaMagneticaUpdate]] = None

    fechas_ica: Optional[List[FechaDict]] = None

    rete_ica: Optional[List[ArticuloUpdate]] = None
    fechas_rete_ica: Optional[List[FechaDict]] = None

    impuesto_industria_comercio: Optional[str] = None

    periodicidad_impuestos: Optional[List[Dict[str, str]]] = None

    # Para almacenar medios magnéticos / información exógena
    informacion_exogena_municipal_medios_magneticos: Optional[List[InfoExogenaMagneticaUpdate]] = None

    vencimiento_declaraciones_x_nit: Optional[List[FechaDict]] = None
    vencimiento_declaraciones_x_nit_ica: Optional[List[FechaDict]] = None
    vencimiento_declaraciones_x_nit_rete_ica: Optional[List[FechaDict]] = None

