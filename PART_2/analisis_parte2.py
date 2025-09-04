import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ─── 1) CARGA DEL CSV DE CATEGORÍAS ─────────────────────────────────────────────
# Asumimos que se ejecuta el script en /app/parte2, así que el CSV está ahí
df_cat = pd.read_csv(
    "../emails_categorizados.csv",
    dtype={"email_id": int}
)

# ─── 2) CONEXIÓN A MySQL PARA FECHAS ─────────────────────────────────────────────
# Cargamos .env de la parte1 para las credenciales
dotenv_path = os.path.abspath(os.path.join("..", "parte1", ".env"))
load_dotenv(dotenv_path)

dbconfig = {
    "host":     os.getenv("DB_HOST", "db"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "atc"),
    "charset":  "utf8mb4",
}

cnx = mysql.connector.connect(**dbconfig)
query = "SELECT id AS email_id, fecha_envio FROM emails;"
df_dates = pd.read_sql(query, con=cnx, parse_dates=["fecha_envio"])
cnx.close()

# ─── 3) COMBINAR Y PREPARAR DATAFRAME ────────────────────────────────────────────
df = pd.merge(df_dates, df_cat, on="email_id", how="inner")
df.set_index("fecha_envio", inplace=True)

print(f"Total correos combinados: {len(df)}")  

# ─── 4) GRÁFICO 1: Volumen por categoría ────────────────────────────────────────
vol = df["categoria"].value_counts().sort_index()

plt.figure(figsize=(8,5))
vol.plot(kind="bar")
plt.title("Volumen de correos por categoría")
plt.xlabel("Categoría")
plt.ylabel("Número de correos")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("volumen_por_categoria.png")
plt.clf()

# ─── 5) GRÁFICO 2: Serie mensual ────────────────────────────────────────────────
por_mes = df.resample("MS")["categoria"].count()


plt.figure(figsize=(8,4))
por_mes.plot(marker="o")
plt.title("Correos por mes")
plt.xlabel("Fecha")
plt.ylabel("Número de correos")
plt.tight_layout()
plt.savefig("correos_por_mes.png")
plt.clf()

# ─── 6) GRÁFICO 3: Día de la semana vs categoría ───────────────────────────────
df["weekday"] = df.index.day_name()
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
pivot = (
    df.groupby("weekday")["categoria"]
      .value_counts()
      .unstack(fill_value=0)
      .reindex(weekdays)
)

plt.figure(figsize=(8,5))
pivot.plot(kind="bar", stacked=True, ax=plt.gca())
plt.title("Correos por categoría y día de la semana")
plt.ylabel("Número de correos")
plt.xticks(rotation=45, ha="right")
plt.legend(bbox_to_anchor=(1.05,1), loc="upper left")
plt.tight_layout()
plt.savefig("correos_por_dia_semana.png")
plt.clf()

print("✔️ Gráficas generadas:")
print("   • volumen_por_categoria.png")
print("   • correos_por_mes.png")
print("   • correos_por_dia_semana.png")
