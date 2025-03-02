from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

# Configurar logger para registrar errores
logger = logging.getLogger("uvicorn.error")

def setup_cors(app: FastAPI):
    """
    Configura CORS de forma restringida.
    Ajusta la lista de orígenes permitidos según el entorno (desarrollo/producción).
    """
    # Lista blanca de orígenes permitidos (cámbiala según tus dominios de confianza)
    origins = [
        "http://localhost:5173/",
        "http://127.0.0.1:8000/",
        "http://localhost:5173"
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,            # No se usa "*" en producción
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

def setup_global_exception_handler(app: FastAPI):
    """
    Configura un middleware global para capturar y registrar excepciones.
    Esto evita que errores internos se propaguen sin control y oculta detalles sensibles.
    """
    @app.middleware("http")
    async def global_exception_handler(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Error en la petición {request.url}: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Ocurrió un error interno en el servidor."},
            )
