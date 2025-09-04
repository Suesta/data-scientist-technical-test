# Parte 4 – Sistema de Clasificación Flexible de Emails

Este módulo implementa un sistema de clasificación automática de emails, **configurable mediante reglas en lenguaje natural** (en español o inglés).  
Evalúa secuencialmente las reglas personalizadas, y si ninguna aplica, delega la clasificación en el servicio REST creado en la Parte 1.

---

## 📂 Estructura de la carpeta

```

parte4/
├── base.py                # Interfaces y lógica base (NO modificar)
├── classifiers.py         # Reglas básicas y secuenciador
├── deserializer.py        # Deserializa config JSON a objetos
├── dependencies.py        # Glue: inyecta parser y deserializer
├── parser.py              # Parser NL (ES/EN) a JSON
├── requirements.txt       # Dependencias mínimas
├── .env                   # Configura URL del servicio Parte 1
├── test.py                # Pruebas unitarias proporcionadas (NO modificar)
└── README.md              # Este archivo

````

> **Puedes borrar sin problema las carpetas `__pycache__` y `.pytest_cache` antes de entregar**. Solo entrega los archivos de arriba.

---

## 🚀 Cómo instalar y ejecutar

1. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
````

2. **Configura el endpoint de la Parte 1:**

   Crea un archivo `.env` (ya incluido) con la siguiente línea:

   ```
   CLASSIFY_URL=http://localhost:8000/classify-email
   ```

   > Este valor asume que tu **Parte 1** (la API REST) está corriendo en local, en el puerto 8000.
   > Si la API está dockerizada y ejecutándose como `atc_app` en la misma red que este módulo, usa:
   > `CLASSIFY_URL=http://atc_app:8000/classify-email`

3. **Lanza los tests para comprobar que todo funciona:**

   ```bash
   python -m pytest -q
   ```

   o

   ```bash
   pytest test.py -q
   ```

   Deberías ver:

   ```
   .......                                                              [100%]
   7 passed in X.XXs
   ```

---

## 🛠️ Detalles y justificación de la entrega

* **Por qué ejecutarlo en local:**
  El sistema de clasificación flexible de la Parte 4 está diseñado para integrarse **directamente** con el endpoint REST ya desarrollado en la Parte 1.
  El revisor puede así lanzar los tests de forma rápida y reproducible en cualquier entorno, sin requerir Docker adicional.
  Si la empresa quisiera dockerizar también esta parte, bastaría añadir un Dockerfile y usar el `.env` correspondiente, pero para una prueba técnica junior, el flujo local es claro y suficiente.

* **No se ha modificado `base.py` ni `test.py`**, cumpliendo el enunciado.

* **El parser NL** soporta reglas en español e inglés, con variantes, y mapea automáticamente los campos y operaciones (`equals`, `contains`).

* **Todos los tests pasan**, cubriendo los escenarios descritos en el enunciado (reglas secuenciales, campos, operaciones, casos límite…).

---

## 💡 Ejemplo rápido de uso

El flujo básico es:

1. **Describe reglas en texto** (“Si el asunto contiene 'urgente', clasifícalo como 'urgente'. …”)
2. **El parser las convierte a JSON estándar.**
3. **El deserializer las transforma en un pipeline de clasificadores.**
4. **El sistema evalúa cada email y devuelve la categoría correcta.**

La integración con la API REST asegura que el sistema es robusto y extensible.

---

## ✅ Entrega pulida y minimalista

* Solo incluye los archivos necesarios, sin artefactos de compilación ni cachés.
