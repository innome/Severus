import os
import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# En modo testing intentamos importar el DummyDatabase de tests/dummies.py.
# Nota: Aunque no es ideal que el código de producción importe módulos de tests,
# en este caso se hace condicionalmente solo cuando TESTING está activo.
if os.getenv("TESTING") == "1":
    try:
        from tests.dummies import DummyDatabase
    except ImportError:
        DummyDatabase = None
else:
    DummyDatabase = None

class Database:
    def __init__(self, mongo_url: str):
        self.mongo_url = mongo_url
        self.client = None
        self.db = None

    async def connect(self):
        # Si estamos en modo testing y contamos con el DummyDatabase, usarlo.
        if os.getenv("TESTING") == "1" and DummyDatabase is not None:
            print("TESTING mode: using DummyDatabase.")
            self.client = None
            self.db = DummyDatabase()
            return

        self.client = AsyncIOMotorClient(self.mongo_url)
        self.db = self.client["microservicio"]
        try:
            # Verificar la conexión intentando enviar el comando "ping".
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

# URL de conexión a MongoDB (en producción)
mongo_url = "mongodb+srv://sasseverus:s2PYwHYd4LXLzp0W@severus-cluster.bgtnf.mongodb.net/?retryWrites=true&w=majority&appName=severus-cluster"
database = Database(mongo_url)

async def registrar_auditoria(microservicio: str, usuario: str, accion: str, detalles: dict):
    """Registrar un evento de auditoría en la base de datos."""
    log = {
        "microservicio": microservicio,
        "usuario": usuario,
        "accion": accion,
        "detalles": detalles,
        "fecha": datetime.datetime.utcnow(),
    }
    await database.db.auditoria.insert_one(log)

def get_collection(collection_name: str):
    """Devuelve una colección si la base de datos está conectada."""
    if database.db is None:
        raise ValueError("La base de datos no está conectada. Llama a 'connect()' antes de usarla.")
    return database.db[collection_name]
