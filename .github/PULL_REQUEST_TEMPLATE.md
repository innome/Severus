
**Checklist para Pull Request**

_Descripción de los cambios_


_General_

 - [ ] La descripción del PR es clara y detalla qué problema se
       resuelve. 
 - [ ] Se incluye el enlace al issue o ticket relacionado (siaplica).
 - [ ] Se explica el alcance y las motivaciones de los cambios.

_Código_

 - [ ] El código sigue los estándares de estilo y convenciones del
       proyecto.
 - [ ] Se han agregado comentarios donde sean necesarios.
 - [ ] Se han refactorizado las partes complicadas o duplicadas del
       código.

_Tests y Calidad_

 - [ ] Se han añadido tests unitarios o funcionales para los nuevos
       cambios.
 - [ ] Todos los tests (nuevos y existentes) pasan correctamente.
 - [ ] Se ha verificado la cobertura de código y se han incluido tests
       en caso de baja cobertura.

_Documentación_

 - [ ] Se ha actualizado la documentación del proyecto (README, Wiki,
       etc.) según corresponda.
 - [ ] Se han incluido instrucciones de uso o ejemplos en caso de
       cambios en la API o funcionalidades.

_Integración y Despliegue_

 - [ ] La configuración de CI/CD está actualizada y no presenta errores
       en la ejecución.
 - [ ] Se han probado los cambios en un entorno de staging o de pruebas,
       si aplica.
 - [ ] Se han considerado las implicaciones en el despliegue y
       migraciones, en caso de cambios en la base de datos u otros
       servicios.

_Seguridad y Rendimiento_

 - [ ] Se han verificado posibles vulnerabilidades y se han aplicado
       medidas de seguridad.
 - [ ] Se han realizado pruebas de rendimiento o se ha evaluado el
       impacto en el rendimiento del sistema.

_Otros_

 - [ ] Se han revisado las dependencias y se actualizó la documentación
       de versiones, si es necesario.
 - [ ] Se ha evaluado el impacto en otras áreas del proyecto para evitar
       efectos colaterales.
 - [ ] Se ha solicitado revisión de otros miembros del equipo, en caso
       de cambios críticos o complejos.
