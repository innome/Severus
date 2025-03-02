# app/controllers/audit_controller.py
from fastapi import APIRouter, Request, HTTPException, Depends
from services.audit_service import log_audit, get_audit_logs
from datetime import datetime
from config.auth import get_current_user

router = APIRouter(prefix="/audit", tags=["Municipios"])

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_audit(request: Request):
    try:
        data = await request.json()
        usuario = data.get("usuario")
        accion = data.get("accion")
        detalles = data.get("detalles", "")
        if not usuario or not accion:
            raise HTTPException(status_code=400, detail="Faltan datos de auditoría")
        await log_audit(usuario, accion, detalles)
        return {"msg": "Auditoría registrada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", dependencies=[Depends(get_current_user)])
async def read_audit_logs():
    try:
        logs = await get_audit_logs()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))