from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import datetime
from typing import List, Optional
from passlib.context import CryptContext


class Database:
    def __init__(self, mongo_url: str):
        self.mongo_url = mongo_url
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client["microservicio"]
        try:
            # Intenta listar las bases de datos para verificar la conexión
            await self.client.admin.command("ping")
            print("Conexión a MongoDB establecida")
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            raise ValueError("No se pudo conectar a la base de datos")


    async def disconnect(self):
        """Cerrar la conexión a MongoDB."""
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada")



# Instancia de la clase Database con tu URL de conexión
mongo_url = "mongodb+srv://sasseverus:s2PYwHYd4LXLzp0W@severus-cluster.bgtnf.mongodb.net/?retryWrites=true&w=majority&appName=severus-cluster"
database = Database(mongo_url)



async def registrar_auditoria(microservicio: str, usuario: str, accion: str, detalles: dict):
    """Registrar un evento de auditoría en la base de datos."""
    log = {
        "microservicio": microservicio,
        "usuario": usuario,
        "accion": accion,
        "detalles": detalles,
        "fecha": datetime.utcnow(),
    }
    await database.db.auditoria.insert_one(log)


def get_collection(collection_name: str):
    """Devuelve una colección si la base de datos está conectada."""
    if database.db is None:  # Validación explícita con None
        raise ValueError("La base de datos no está conectada. Llama a 'connect()' antes de usarla.")
    return database.db[collection_name]