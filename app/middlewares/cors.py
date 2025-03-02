# middlewares/cors.py
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response

def setup_cors(app: FastAPI):
    """
    Aplica las configuraciones de CORS a la instancia de FastAPI
    y configura la instrumentación con OpenTelemetry.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
