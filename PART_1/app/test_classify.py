import os
import sys

# Asegura que el directorio padre (donde está main.py) esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import classify_text

@pytest.mark.parametrize("text, expected", [
    # Pagos y Cobros
    ("Necesito realizar un pago a mi factura", "Pagos y Cobros"),
    # Incidencias Técnicas
    ("Hay un error en el servidor al cargar datos", "Incidencias Técnicas"),
    # Facturación
    ("¿Me pueden enviar el desglose de mi factura?", "Facturación"),
    # Información Comercial
    ("Quiero conocer las ofertas y promociones vigentes", "Información Comercial"),
    # Contrato y Titularidad
    ("Deseo dar de baja mi contrato inmediatamente", "Contrato y Titularidad"),
    # Lecturas de Consumo
    ("¿Cuál es mi lectura de consumo de este mes?", "Lecturas de Consumo"),
    # Acceso y Cuenta
    ("Olvidé mi contraseña y no puedo acceder", "Acceso y Cuenta"),
    # Otras Consultas
    ("Buenas tardes, ¿me pueden atender?", "Otras Consultas"),
    # Caso vacío
    ("", "Otras Consultas"),
])
def test_classify(text, expected):
    assert classify_text(text) == expected
