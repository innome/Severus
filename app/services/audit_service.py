# app/services/audit_service.py
from datetime import datetime
from models.audit_log_model import AuditLog
from config.database import get_collection


AUDIT_COLLECTION = "audit_logs"

async def log_audit(usuario: str, accion: str, detalles: str):
    audit = AuditLog(
        usuario=usuario,
        accion=accion,
        detalles=detalles,
        fecha_hora=datetime.utcnow()
    )
    try:
        audit_collection = get_collection(AUDIT_COLLECTION)
        await audit_collection.insert_one(audit.dict())
    except Exception as e:
        # Aquí puedes registrar el error en un log
        print("Error al registrar auditoría:", e)


async def get_audit_logs():
    logs = []
    try:
        audit_collection = get_collection(AUDIT_COLLECTION)
        # Se obtienen los documentos ordenados por fecha_hora descendente
        async for doc in audit_collection.find().sort("fecha_hora", -1):
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            logs.append(doc)
    except Exception as e:
        print("Error al obtener logs:", e)
        raise e
    return logs