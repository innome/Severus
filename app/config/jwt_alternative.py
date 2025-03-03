import os
import json
import base64
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, hmac  # Usamos hmac de cryptography para HMAC-HASH
import hmac as std_hmac  # Importamos el módulo estándar para compare_digest

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"  # Solo soportamos HS256 en este ejemplo

def base64url_encode(data: bytes) -> str:
    """Codifica en base64 URL-safe sin padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(input_str: str) -> bytes:
    """Decodifica de base64 URL-safe agregando padding si es necesario."""
    rem = len(input_str) % 4
    if rem:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str.encode('utf-8'))

def create_token(payload: dict, expires_delta: timedelta = None) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    payload["exp"] = int(expire.timestamp())
    
    header_json = json.dumps(header, separators=(",", ":")).encode('utf-8')
    payload_json = json.dumps(payload, separators=(",", ":")).encode('utf-8')
    
    header_b64 = base64url_encode(header_json)
    payload_b64 = base64url_encode(payload_json)
    
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    
    # Crear firma usando HMAC-SHA256 (de cryptography)
    h = hmac.HMAC(SECRET_KEY.encode('utf-8'), hashes.SHA256())
    h.update(message)
    signature = h.finalize()
    signature_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_token(token: str) -> dict:
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Token mal formado")
    
    header_b64, payload_b64, signature_b64 = parts
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    
    h = hmac.HMAC(SECRET_KEY.encode('utf-8'), hashes.SHA256())
    h.update(message)
    expected_signature = h.finalize()
    
    # Usamos std_hmac.compare_digest para comparar de forma segura
    if not std_hmac.compare_digest(expected_signature, base64url_decode(signature_b64)):
        raise ValueError("Firma inválida")
    
    payload_json = base64url_decode(payload_b64)
    payload = json.loads(payload_json)
    
    exp = payload.get("exp")
    if exp is None or int(time.time()) > exp:
        raise ValueError("Token expirado")
    
    return payload
