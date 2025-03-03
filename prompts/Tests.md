Actúa como un experto en desarrollo de software y testing. Quiero que generes una suite completa de tests para el siguiente fragmento de código. Analiza cuidadosamente el código, identifica sus funcionalidades, dependencias y casos de uso, y genera pruebas unitarias y de integración utilizando frameworks estándar como pytest (y, si aplica, FastAPI TestClient para endpoints web). Asegúrate de incluir:

1.  **Tests unitarios:**
    
    *   Pruebas para cada función o método, cubriendo tanto escenarios positivos como negativos.
        
    *   Uso de fixtures de pytest y mocks o dummies para simular dependencias externas (por ejemplo, bases de datos, servicios externos o librerías específicas).
        
    *   Pruebas parametrizadas (table-driven tests) para escenarios que involucren múltiples casos de entrada/salida.
        
2.  **Tests de integración (si el código es parte de una aplicación web):**
    
    *   Uso de FastAPI TestClient (u otro cliente similar) para simular llamadas a endpoints.
        
    *   Validación de respuestas HTTP (status code, estructura JSON, encabezados, etc.) y de comportamientos de seguridad (por ejemplo, autenticación).
        
3.  **Buenas prácticas:**
    
    *   Código de test claro y comentado.
        
    *   Estructura del proyecto de tests sugerida (por ejemplo, separar tests unitarios en un archivo y tests de integración en otro, o usar un archivo 'conftest.py' para configurar fixtures globales).
        
    *   Consideraciones para sobrescribir comportamientos críticos en ambiente de test (por ejemplo, evitar conexiones reales a bases de datos mediante el uso de dummies o mocks).
        

Genera una suite de tests completa para el siguiente fragmento de código, incluyendo ejemplos de cómo estructurar y organizar los archivos de tests. Solo usa el fragmento de código que te proporcionaré y asegúrate de que las pruebas sean autoexplicativas y puedan copiarse y ejecutarse en cualquier entorno.