import os
import time
import re

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import pooling

# 1. Carga de variables de entorno
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "atc")

# 2. Configuración de parámetros de conexión (para el pool)
dbconfig = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "charset": "utf8mb4",
}

# 3. Inicialización de la aplicación FastAPI
app = FastAPI(title="ATC Email Classifier")
cnxpool = None  # Se instanciará en el evento de arranque

# 4. Evento de arranque para crear el pool con reintentos
@app.on_event("startup")
def startup_db_pool():
    global cnxpool
    retries = 10
    while retries > 0:
        try:
            cnxpool = pooling.MySQLConnectionPool(
                pool_name="atc_pool",
                pool_size=5,
                **dbconfig
            )
            # Verificación de conexión rápida
            conn = cnxpool.get_connection()
            conn.close()
            print("✅ Conexión a MySQL establecida.")
            return
        except mysql.connector.Error as e:
            retries -= 1
            print(f"⏳ Esperando a MySQL ({10-retries}/10), error: {e}")
            time.sleep(5)
    raise RuntimeError("❌ No se pudo conectar a MySQL tras varios intentos.")

# 5. Modelo de datos de la petición
class EmailRequest(BaseModel):
    client_id: int
    fecha_envio: str       # formato "YYYY-MM-dd hh:mm:ss"
    email_body: str


# 6. Función de clasificación por reglas (ordenada para prioridades)
def classify_text(text: str) -> str:
    t = text.lower()

    # 6.1 Pagos y Cobros (prioridad máxima)
    if re.search(r"\b(impago|pago|pagos|cobro|cobros|regulariz|erróneo|duplic|cargo|cargos)\b", t):
        return "Pagos y Cobros"

    # 6.2 Contrato y Titularidad (subimos contrato/contratar, titularidad, baja, alta)
    if re.search(r"\b(contrat\w*|titularidad|baja|alta)\b", t):
        return "Contrato y Titularidad"

    # 6.3 Incidencias Técnicas
    if re.search(
        r"\b(error|fallo|servidor|imposibil|corte|suministro"
        r"|incidencia|asistencia|t[eé]cnic\w*)\b",
        t
        ):
        return "Incidencias Técnicas"

    # 6.4 Facturación (factura(s), facturación, importe, desglose)
    if re.search(r"\b(facturaci[oó]n|factura|facturas|importe|desglose|facturacion|facturación)\b", t):
        return "Facturación"

    # 6.5 Información Comercial (tarifa(s), oferta(s), promoción(es), contratar, plan)
    if re.search(r"\b(tarifa|tarifas|oferta|ofertas|promoci[oó]n|promociones|contratar|plan|planes)\b", t):
        return "Información Comercial"

    # 6.6 Lecturas de Consumo (lectura(s), consumo(s))
    if re.search(r"\b(lectura|lecturas|consumo|consumos)\b", t):
        return "Lecturas de Consumo"

    # 6.7 Acceso y Cuenta (login, contraseña, acced, registro, cliente)
    if re.search(r"\b(login|contraseñ[ao]|acced|registro|cuenta)\b", t):
        return "Acceso y Cuenta"

    # 6.8 Otras Consultas (por defecto)
    return "Otras Consultas"





# 7. Endpoint POST /classify-email
@app.post("/classify-email")
def classify_email(req: EmailRequest):
    # 7.1 Obtener conexión del pool
    conn = cnxpool.get_connection()
    cursor = conn.cursor()

    # 7.2 Comprobar impagos
    cursor.execute(
        "SELECT COUNT(*) FROM impagos WHERE client_id = %s",
        (req.client_id,)
    )
    (count_impagos,) = cursor.fetchone()
    if count_impagos > 0:
        cursor.close()
        conn.close()
        return {"exito": False, "razon": "El cliente tiene impagos"}

    # 7.3 Registrar el email en la base de datos
    cursor.execute(
        """
        INSERT INTO emails (fecha_envio, client_id, email)
        VALUES (%s, %s, %s)
        """,
        (req.fecha_envio, req.client_id, req.email_body)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # 7.4 Clasificar el contenido
    pred = classify_text(req.email_body)

    # 7.5 Devolver respuesta
    return {"exito": True, "prediccion": pred}
