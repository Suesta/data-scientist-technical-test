# --- 1. Base image ---
FROM python:3.9

# --- 2. Directorio de trabajo ---
WORKDIR /app

# --- 3. Copiar y instalar dependencias de la API ---
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- 4. Instalar librerías para el notebook y análisis ---
RUN pip install --no-cache-dir \
    notebook nbconvert \
    pandas matplotlib mysql-connector-python python-dotenv

# --- 5. Copiar scripts y el resto de la aplicación ---
COPY scripts/ ./scripts/
COPY . .

# --- 6. Exponer el puerto de la API ---
EXPOSE 8000

# --- 7. Comando por defecto para arrancar Uvicorn ---
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
