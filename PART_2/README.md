# Parte 2 – Análisis y Visualización de Correos Categorizados

## Nota sobre el formato notebook (.ipynb)

Según el enunciado, el análisis debía entregarse idealmente en formato Jupyter Notebook (`analisis_parte2.ipynb`).  
Sin embargo, por incompatibilidades técnicas en mi entorno de desarrollo (problemas de dependencias de Jupyter y/o limitaciones de ejecución dentro de Docker/VSCode), **no ha sido posible ejecutar correctamente el análisis y la generación de gráficos en formato notebook**.

Por este motivo, entrego:

- El script `analisis_parte2.py`, que realiza todo el análisis y genera los gráficos de manera reproducible.
- El informe `INFORME_RESULTADOS.md`, que incluye los resultados, los gráficos generados y las conclusiones detalladas. Este documento equivaldría al notebook que se desea, pero ya generado y solo con los comentarios.
- Los archivos de gráficos (`volumen_por_categoria.png`, `correos_por_mes.png`, `correos_por_dia_semana.png`), ya generados y listos para revisión.

Así, garantizo que cualquier persona pueda revisar el código y los resultados sin depender de un entorno notebook concreto.  
En caso de poder ejecutarse en un notebook, todo el análisis y comentarios pueden transferirse fácilmente, pero en este caso se priorizó la robustez y reproducibilidad del análisis.

---

## Archivos incluidos

- `analisis_parte2.py`: Script principal que genera los gráficos y cruza los datos del CSV de categorías con las fechas reales de la base de datos.
- `emails_categorizados.csv`: CSV generado a partir del clasificador de la Parte 1 (debe estar en `/app` al ejecutar el script).
- `volumen_por_categoria.png`, `correos_por_mes.png`, `correos_por_dia_semana.png`: Gráficos generados por el script.
- `INFORME_RESULTADOS.md`: Informe de resultados con el análisis y las recomendaciones, incluyendo los gráficos.

## Requisitos

- Python 3.x (recomendado: usar el mismo entorno del contenedor Docker)
- Paquetes: `pandas`, `matplotlib`, `mysql-connector-python`, `python-dotenv`
- Acceso a la base de datos MySQL levantada por Docker Compose (con las tablas y datos del ejercicio)

## Pasos para regenerar los gráficos

1. **Asegúrate de que el contenedor de la aplicación está en marcha**  
   (desde la raíz de la entrega, normalmente con:)
   ```sh
   docker compose up -d
````

2. **Coloca el archivo `emails_categorizados.csv` actualizado** en `/app`
   (Puedes regenerarlo ejecutando el script de la Parte 1).

3. **Accede al contenedor de la app**

   ```sh
   docker compose exec app bash
   ```

4. **Entra en la carpeta `/app/parte2`**

   ```sh
   cd /app/parte2
   ```

5. **Ejecuta el script de análisis**

   ```sh
   python3 analisis_parte2.py
   ```

6. **Los archivos PNG se generarán en esta misma carpeta**
   (`volumen_por_categoria.png`, `correos_por_mes.png`, `correos_por_dia_semana.png`)

7. **Puedes copiar los archivos de vuelta a tu equipo local si lo necesitas:**
   (Ejemplo para Windows PowerShell)

   ```powershell
   docker cp atc_app:/app/parte2/volumen_por_categoria.png "C:\ruta\local\parte2\volumen_por_categoria.png"
   ```

---

## Notas

* El script cruza automáticamente los IDs del CSV con las fechas reales de la base de datos MySQL, asegurando que sólo se analizan los correos válidos.
* Puedes editar el script `analisis_parte2.py` si deseas personalizar los gráficos o el análisis.
* Para dudas o reproducibilidad, consulta el `INFORME_RESULTADOS.md`.

```

