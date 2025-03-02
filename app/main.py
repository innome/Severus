# main.py

from fastapi import FastAPI
import uvicorn

# Importa la configuración de la base de datos
from config.database import database  

# Importa los controladores
from controllers.user_controller import router as user_router
from controllers.municipios_controller import router as municipios_router
from controllers.tributaria_versionada_controller import router as tributaria_router
from controllers.audit_controller import router as audit_router

# Importa la función para configurar CORS
from middlewares.cors import setup_cors

def create_app() -> FastAPI:
    """
    Crea y configura la instancia principal de la aplicación FastAPI.
    """
    app = FastAPI()

    # Configurar CORS
    setup_cors(app)
    # Eventos de inicio y cierre
    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    # Rutas base de prueba
    @app.get("/")
    def read_root():
        return {"message": "FastAPI está funcionando con MongoDB!"}

    # Incluir los routers
    app.include_router(audit_router)
    app.include_router(municipios_router)
    app.include_router(tributaria_router)
    app.include_router(user_router)

    return app

# Instancia global de la app para ser usada por uvicorn
app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
