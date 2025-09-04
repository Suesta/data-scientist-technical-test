# Parte 1 – Clasificador de Emails

Servicio REST que clasifica correos de clientes en 8 categorías relevantes de negocio y excluye automáticamente a clientes con impagos, facilitando la gestión eficiente de Atención al Cliente.

---

## 🛠️ Prerrequisitos

- **Docker & Docker Compose**  
  (para levantar todo el entorno sin complicaciones)
- **(Opcional) Python 3.9+**  
  Para ejecutar localmente los scripts de generación de CSV y las pruebas unitarias.

---

## 📂 Estructura de carpetas

```

parte1/
├── app/
│   ├── main.py
│   ├── scripts/
│   │   └── generate\_csv.py
│   ├── tests/
│   │   └── test\_classify.py
│   ├── .env                # variables de conexión
│   ├── Dockerfile
│   ├── requirements.txt
├── mysql/
│   └── init.sql            # script de inicialización de MySQL
├── docker-compose.yml      # define servicios atc\_app y mysql\_db
├── emails\_categorizados.csv  # CSV generado (fuera de /app)
├── JUSTIFICACION\_PARTE1.md
└── README.md

````

---

## 🚀 Despliegue rápido

Desde la carpeta raíz, ejecuta:

```bash
docker compose up --build -d
````

Esto levantará los servicios de base de datos y API, y cargará todos los datos iniciales.
Puedes comprobar el estado y logs con:

```bash
docker compose logs -f
```

---

## 🔌 API

**Endpoint**: `POST /classify-email`
**Content-Type**: `application/json`

La API estará disponible en `http://localhost:8000`.

> La documentación interactiva (Swagger UI) está disponible en `http://localhost:8000/docs`.

### Ejemplo de request

```json
{
  "client_id": 3,
  "fecha_envio": "2025-06-29 12:00:00",
  "email_body": "Necesito el desglose de mi factura"
}
```

### Ejemplo de respuesta (200 OK)

* **Cliente sin impagos**

  ```json
  { "exito": true, "prediccion": "<Categoría>" }
  ```
* **Cliente con impagos**

  ```json
  { "exito": false, "razon": "El cliente tiene impagos" }
  ```

---

## 🧪 Pruebas unitarias

Para ejecutar los tests de clasificación:

```bash
# Desde la raíz del proyecto
docker exec -it atc_app bash
pytest -q
exit
```

---

## 📡 Ejemplos de llamada al endpoint

```bash
# Linux/macOS (curl)
curl -X POST http://localhost:8000/classify-email \
  -H "Content-Type: application/json" \
  -d '{"client_id":3,"fecha_envio":"2025-06-29 12:00:00","email_body":"Necesito el desglose de mi factura"}'

# Windows PowerShell
$body = @{
  client_id   = 3
  fecha_envio = "2025-06-29 12:00:00"
  email_body  = "Necesito el desglose de mi factura"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/classify-email `
  -Method Post `
  -ContentType application/json `
  -Body $body
```

> **Nota:** si en tu `docker-compose.yml` usas otros nombres de servicio distintos a `atc_app` y `mysql_db`, reemplázalos en los comandos `docker exec` y `docker cp`.

---

## 📊 Generar CSV de resultados

Para crear `emails_categorizados.csv` (solo incluye emails de clientes reales y sin impagos):

```bash
# 1) Entra al contenedor de la app
docker exec -it atc_app bash

# 2) Ejecuta el script
python scripts/generate_csv.py

# 3) Sal del contenedor y copia el CSV al host
exit
docker cp atc_app:/app/emails_categorizados.csv ./emails_categorizados.csv
```

**Nota:**
El CSV generado sólo incluye emails que pertenecen a clientes existentes (`client_id` ≤ 46) y que no tienen impagos.
No hay registros "fantasma" ni datos inconsistentes en la base de datos, asegurando máxima calidad y limpieza del dataset.

---

## 📂 Categorías de clasificación

| Categoría                  | Keywords (regex)                                                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Pagos y Cobros**         | `impago(s)?`, `pago(s)?`, `cobro(s)?`, `regulariz`, `erróneo`, `duplic`, `cargo(s)?`                             |
| **Contrato y Titularidad** | `contrat\w*`, `titularidad`, `baja`, `alta`                                                                      |
| **Incidencias Técnicas**   | `error`, `fallo`, `servidor`, `imposibil`, `corte(s)?`, `suministro`, `incidencia`, `asistencia`, `t[eé]cnic\w*` |
| **Facturación**            | `facturaci[oó]n`, `factura(s)?`, `importe`, `desglose`                                                           |
| **Información Comercial**  | `tarifa(s)?`, `oferta(s)?`, `promoci[oó]n(es)?`, `contratar`, `plan(es)?`                                        |
| **Lecturas de Consumo**    | `lectura(s)?`, `consumo(s)?`                                                                                     |
| **Acceso y Cuenta**        | `login`, `contraseñ[ao]`, `acced`, `registro`, `cuenta`, `cliente`                                               |
| **Otras Consultas**        | (por defecto)                                                                                                    |

---
