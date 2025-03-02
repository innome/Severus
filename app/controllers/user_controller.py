from fastapi import APIRouter, HTTPException, Depends
from models.usuario_model import UsuarioModel, LoginRequest
from services.usuario_service import crear_usuario, obtener_usuario_por_username, verificar_credenciales
from fastapi.security import OAuth2PasswordRequestForm
from config.auth import create_access_token, get_current_user
from datetime import timedelta

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro")
async def registrar_usuario(usuario: UsuarioModel):
    usuario_existente = await verificar_credenciales(usuario.username, usuario.password)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    usuario_id = await crear_usuario(usuario)
    return {"message": "Usuario registrado exitosamente", "id": usuario_id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Inicio de sesión para usuarios."""
    # Extraer username y password del formulario
    username = form_data.username
    password = form_data.password

    # Verificar credenciales
    usuario = await verificar_credenciales(username, password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Generar token de acceso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": usuario.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", dependencies=[Depends(get_current_user)])
async def list_examples():
    """Ruta protegida para listar ejemplos."""
    return {"message": "Solo usuarios autenticados pueden acceder a esta ruta"}