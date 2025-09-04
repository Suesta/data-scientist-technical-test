import os
import sys

# Aseguramos que /app (el padre de scripts) está en sys.path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import csv
import time
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

# Importamos la función de clasificación desde main.py
from main import classify_text

# Carga de variables de entorno
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "atc")

# Configuración de conexión
dbconfig = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "charset": "utf8mb4",
}

# Creamos la conexión
cnx = mysql.connector.connect(**dbconfig)
cursor = cnx.cursor()

# 1) Recuperar lista de clientes morosos
cursor.execute("SELECT client_id FROM impagos")
morosos = {row[0] for row in cursor.fetchall()}

# 2) Recuperar todos los emails con su client_id
cursor.execute("SELECT id, client_id, email FROM emails")
rows = cursor.fetchall()

# Ruta de salida
output_path = os.path.join(os.path.dirname(__file__), "..", "emails_categorizados.csv")

# 3) Escritura del CSV, excluyendo impagos
with open(output_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["email_id", "categoria"])
    for email_id, client_id, email_body in rows:
        # Saltar si pertenece a cliente moroso
        if client_id in morosos:
            continue
        categoria = classify_text(email_body)
        writer.writerow([email_id, categoria])

print(f"✅ CSV generado en: {output_path}")

cursor.close()
cnx.close()
