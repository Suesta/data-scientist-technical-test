# Justificación Técnica – Parte 1

Como candidato al puesto de Data Scientist Junior, he diseñado esta solución priorizando la velocidad de entrega, la claridad del código, la reproducibilidad del entorno y la facilidad de mantenimiento futuro.

1. **Elección de FastAPI**
   Opté por FastAPI por su rendimiento asíncrono, la generación automática de documentación (OpenAPI/Swagger) y la validación estricta de entradas gracias a Pydantic. Esto permitió montar el endpoint `/classify-email` de forma sencilla, segura y documentada, garantizando la calidad de los datos recibidos.

2. **Definición de categorías de negocio**
   Identifiqué ocho categorías clave (**Facturación**, **Pagos y Cobros**, **Información Comercial**, **Contrato y Titularidad**, **Lecturas de Consumo**, **Acceso y Cuenta**, **Incidencias Técnicas** y **Otras Consultas**) buscando un equilibrio entre granularidad y simplicidad, de modo que la clasificación aporte valor real a la operativa del departamento.

3. **Clasificador rule-based con pruebas unitarias**
   Ante la ausencia de un dataset etiquetado suficiente para Machine Learning, implementé un clasificador basado en reglas mediante expresiones regulares, fácilmente extensible en futuras versiones.

   * Las reglas están ordenadas por prioridad: primero detecta términos de impago y pagos, después cuestiones contractuales, a continuación incidencias técnicas, y así sucesivamente.
   * Incluyen patrones Unicode y variantes para cubrir tildes, plurales y errores habituales.
   * Añadí un conjunto de **pruebas unitarias** (`tests/test_classify.py`) que validan los principales casos de uso y previenen regresiones ante futuras modificaciones.

4. **Filtrado de impagos antes de la clasificación**
   La API consulta primero la tabla `impagos`; si detecta deudas, devuelve `{ "exito": false, "razon": "El cliente tiene impagos" }` y detiene el procesamiento, cumpliendo el requisito de excluir automáticamente estos casos.

5. **Depuración y limpieza de la base de datos inicial**
   Durante la fase de integración, detecté que varios correos y registros de impagos hacían referencia a `client_id` superiores a 46, los cuales no existen en la definición original de la tabla de clientes.
   En vez de añadir "clientes fantasma" para satisfacer integridad referencial (lo cual generaba ruido y resultados no representativos), **he optado por limpiar y corregir los datos**:

   * **He eliminado de la base de datos todos los correos y referencias asociadas a `client_id > 46`**, asegurando así que todos los registros utilizados sean consistentes y reflejen únicamente clientes reales.
   * Esta solución elimina problemas futuros, evita datos basura y garantiza que la lógica de negocio y el análisis sean fiables, reproducibles y auditables.

6. **Contenerización con Docker y Docker Compose**
   Preparé un `Dockerfile` para la aplicación Python y un `docker-compose.yml` que levanta MySQL (ejecutando `init.sql`) y el servicio FastAPI en un solo comando:

   ```bash
   docker compose up --build -d
   ```

---