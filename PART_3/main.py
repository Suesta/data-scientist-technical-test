import os
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv

# ─── 1. LEER CLAVES DESDE .env ───────────────────────────────────────────────────
load_dotenv()                         
openai.api_key = os.getenv("OPENAI_API_KEY")

# ─── 2. CONFIGURACIÓN DE LA API DE CLASIFICACIÓN ────────────────────────────────
CLASSIFY_URL = os.getenv(
    "CLASSIFY_URL",
    "http://localhost:8000/classify-email"
)

# ─── 3. FUNCIÓN DE CLASIFICACIÓN ────────────────────────────────────────────────
def classify_email(client_id: int, fecha_envio: str, email_body: str) -> str:
    """
    Llama al endpoint /classify-email de la Parte 1 y devuelve
    la categoría o "Moroso" si el backend responde exito=False.
    """
    payload = {
        "client_id":   client_id,
        "fecha_envio": fecha_envio,
        "email_body":  email_body
    }
    resp = requests.post(CLASSIFY_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("exito", True):
        return "Moroso"
    return data["prediccion"]

# ─── 4. PLANTILLAS BASE PARA BORRADORES ─────────────────────────────────────────
BASE_RESPONSES = {
    "Contrato y Titularidad": (
        "Buenas tardes, gracias por su consulta. "
        "Puede descargar su contrato de electricidad y gas directamente "
        "desde nuestra aplicación móvil o desde el área de clientes en nuestra página web."
    ),
    "Pagos y Cobros": (
        "Buenos días, gracias por su consulta. "
        "Puede encontrar y descargar copias de todas las facturas asociadas a sus contratos "
        "en nuestra aplicación móvil o en el área de clientes en nuestra página web."
    ),
    "Información Comercial": (
        "Hola, gracias por su interés. "
        "Toda la información sobre nuestras tarifas actuales para nuevos clientes "
        "está disponible en nuestra página web de Factor Energía."
    ),
    "Incidencias Técnicas": (
        "Hola, gracias por contactarnos. "
        "Un agente revisará el problema que indica con el suministro de electricidad tan pronto como sea posible "
        "y se pondrá en contacto con usted."
    ),
}

# ─── 5. GENERAR BORRADOR CON GPT ─────────────────────────────────────────────────
def generate_reply(email_body: str, category: str) -> str:
    """
    Toma la plantilla base según categoría y la enriquece con GPT.
    Si es Moroso o categoría desconocida, usa un texto alternativo.
    """
    if category in BASE_RESPONSES:
        prompt = (
            f"Toma esta plantilla para la categoría «{category}»:\n\n"
            f"{BASE_RESPONSES[category]}\n\n"
            f"Y adáptala de forma natural al siguiente correo del cliente:\n"
            f"{email_body}"
        )
    elif category == "Moroso":
        return (
            "Hola, gracias por su mensaje. "
            "Hemos detectado que actualmente tiene pagos pendientes. "
            "Por favor, regularice su situación y un agente se pondrá en contacto con usted."
        )
    else:
        return (
            "Hola, gracias por su mensaje. Un agente de Atención al Cliente revisará su consulta "
            "y se pondrá en contacto con usted lo antes posible."
        )

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente de Atención al Cliente de Factor Energía."},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

# ─── 6. FLUJO PRINCIPAL ─────────────────────────────────────────────────────────
def main() -> None:
    tests = [
        (3,  "Hola buenas tardes, necesito que me envíen el contrato de electricidad y gas. Nunca me lo han enviado.", "Contrato y Titularidad"),
        (25, "Hola, buenos días. Mira que me habéis cobrado las facturas de la luz y el gas, pero no me habéis mandado la factura. Gracias.", "Pagos y Cobros"),
        (12, "Buenas, quisiera conocer las tarifas actuales para nuevos clientes.", "Información Comercial"),
        (6,  "Buenos días, he tenido un problema con el suministro de electricidad. Por favor, ayúdenme.", "Incidencias Técnicas"),
        (7,  "Hola, ¿me pueden explicar cómo cambiar mis datos de contacto?", "Genérico"),
        # Caso moroso:
        (8,  "Hola, tengo problemas para acceder a mi factura online.", "Moroso"),
    ]


    for client_id, body, desc in tests:
        print("────────────────────────────────────────")
        print(f"📥 Caso: {desc}")
        print(f"👤 Client ID: {client_id}")
        categoria = classify_email(
            client_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            body
        )
        print("📂 Categoría detectada:", categoria)
        borrador = generate_reply(body, categoria)
        print("✉️ Borrador de respuesta:\n", borrador)
    print("✅ Todos los casos ejecutados.")

if __name__ == "__main__":
    main()
