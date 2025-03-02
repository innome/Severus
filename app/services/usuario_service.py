from config.database import get_collection
from models.usuario_model import UsuarioModel
from bson import ObjectId


async def crear_usuario(usuario: UsuarioModel):
    collection = get_collection("usuarios")
    # Hashear la contraseña antes de guardar
    usuario.hash_password()
    result = await collection.insert_one(usuario.dict())
    return str(result.inserted_id)

async def obtener_usuario_por_username(username: str):
    collection = get_collection("usuarios")
    documento = await collection.find_one({"username": username})
    if documento:
        return UsuarioModel(**documento)
    return None

async def verificar_credenciales(username: str, password: str):
    usuario = await obtener_usuario_por_username(username)
    if usuario and usuario.verificar_password(password):
        return usuario
    return None
