
## Prompt Mejorado: Severus App

Este proyecto se denomina **Severus**, y su propósito es manejar la lógica de una aplicación FastAPI, organizando la información tributaria versionada, la autenticación, la auditoría y los servicios relacionados con municipios y usuarios.

### 1. Estructura General

└── 📁Severus
    └── 📁.github
        └── 📁workflows
            └── backport.yml
            └── ci.yml
    └── 📁app
        └── __init__.py
        └── .env
        └── 📁config
            └── __init__.py
            └── auth.py
            └── database.py
            └── jwt_alternative.py
        └── 📁controllers
            └── __init__.py
            └── audit_controller.py
            └── municipios_controller.py
            └── tributaria_versionada_controller.py
            └── user_controller.py
        └── main.py
        └── 📁middlewares
            └── __init__.py
            └── cors.py
        └── 📁models
            └── __init__.py
            └── audit_log_model.py
            └── informacion_tributaria_versionada_update_model.py
            └── municipios_model.py
            └── tributaria_versionada_model.py
            └── usuario_model.py
        └── 📁services
            └── __init__.py
            └── audit_service.py
            └── municipios_service.py
            └── tributaria_versionada_service.py
            └── usuario_service.py
        └── 📁tests
            └── __init__.py
            └── conftest.py
            └── dummies.py
            └── test_main.py
            └── test_municipios_controller.py
            └── test_municipios_service.py
            └── test_user_controller.py
            └── test_usuario_service.py
    └── 📁prompts
        └── test.md
    └── .gitignore
    └── README.md
    └── requirements.txt


### 2. Preparación del Entorno

-   **Activar el entorno virtual**:

    `cd Severus`
    `venv\Scripts\activate   # En Windows`
    o
    `source venv/bin/activate  # En Linux/Mac`
    
-   **Instalar dependencias**:

    `pip install -r requirements.txt` 
    

### 3. Arrancar la Aplicación

En la carpeta `app` se encuentra el archivo `main.py`, que sirve como punto de entrada de FastAPI:

    uvicorn main:app --reload 

Una vez iniciado, la API estará disponible en:

    http://127.0.0.1:8000

### 4. Ejecutar Pruebas

El proyecto incluye pruebas automatizadas en la carpeta `tests`. Para ejecutarlas con Pytest:

    cd Severus/app
    python -m pytest tests 

De esta manera se validan los controladores, servicios y la lógica de negocio definida.

### 5. Descripción de Componentes Clave

1.  **`config`**: Maneja la configuración principal (base de datos, autenticación, JWT).
2.  **`controllers`**: Define los endpoints de la API (audit_controller, municipios_controller, tributaria_versionada_controller, user_controller).
3.  **`middlewares`**: Aplica lógica de pre o post-procesamiento, como el CORS.
4.  **`models`**: Contiene los modelos de datos (Pydantic) para la información tributaria, usuarios, etc.
5.  **`services`**: Implementa la lógica de negocio y acceso a la base de datos.
6.  **`tests`**: Aloja los archivos de pruebas unitarias/integrales.
