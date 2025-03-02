# app/models/audit_log_model.py
from datetime import datetime
from pydantic import BaseModel

class AuditLog(BaseModel):
    usuario: str
    accion: str
    detalles: str
    fecha_hora: datetime
