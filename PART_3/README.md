# Parte 3: Generación de Borradores de Respuesta

Este módulo toma un correo de cliente, lo clasifica usando el endpoint REST de la Parte 1, y genera automáticamente un borrador de respuesta adaptada mediante GPT-4o-mini (OpenAI).

---

## 📂 Estructura del proyecto

```text
parte3/
├── main.py           # Lógica de clasificación + generación de respuesta
├── requirements.txt  # openai, requests, python-dotenv
├── .env              # Variables de entorno: OPENAI_API_KEY, CLASSIFY_URL
└── README.md
```

---

## 🛠️ Instalación

Desde la carpeta `parte3`:

```bash
pip install -r requirements.txt
```

*(Asegúrate de tener Python 3.9 o superior y pip instalado)*

---

## 🔧 Configuración

1. Crea un fichero `.env` con el siguiente contenido:

   ```ini
   OPENAI_API_KEY=sk-...
   CLASSIFY_URL=http://localhost:8000/classify-email
   ```

2. Asegúrate de que la **API de clasificación** (Parte 1) está corriendo y accesible en la URL indicada en `CLASSIFY_URL`.
   *(Recomendado: ejecuta `docker compose up -d` en la Parte 1 antes de probar la Parte 3).*

---

## 🚀 Uso

```bash
python main.py
```

Por cada caso de prueba verás en consola:

```
📥 Caso: <Descripción>
👤 Client ID: <id>
📂 Categoría detectada: <Categoría>
✉️ Borrador de respuesta:
  <Texto generado>
```

---

## 🎯 Casos de prueba incluidos

| Caso                   | Client ID | Descripción                |
| ---------------------- | --------- | -------------------------- |
| Contrato y Titularidad | 3         | Cliente al día             |
| Pagos y Cobros         | 25        | Cliente al día (no moroso) |
| Información Comercial  | 12        | Cliente al día             |
| Incidencias Técnicas   | 6         | Cliente al día             |
| Genérico               | 7         | Cliente al día             |
| Moroso                 | 8         | Cliente con impagos        |

> **Nota sobre morosos:**
> Si usas un `client_id` con impagos (por ejemplo 8, 16, 47–50 según la base de datos de la Parte 1), la API responderá:
>
> ```jsonc
> { "exito": false, "razon": "El cliente tiene impagos" }
> ```
>
> y el sistema devolverá un texto amable pidiendo regularizar la deuda antes de poder tramitar la consulta.

---

## ⚠️ Límite de llamadas

El modelo `gpt-4o-mini` de OpenAI tiene cuota limitada. Ejecuta **solo las pruebas necesarias** para evitar consumir tu saldo.

---

## ✏️ Personalización

* **API de clasificación**: cambia `CLASSIFY_URL` en el `.env` si tu backend corre en otra URL o puerto.
* **Casos de prueba**: edita la lista `tests` en `main.py` para añadir o modificar ejemplos y adaptar los flujos a tus necesidades.

---

