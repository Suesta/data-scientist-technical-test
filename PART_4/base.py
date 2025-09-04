import os
import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

@dataclass
class Email:
    client_id: int
    subject: str
    body: str
    sender: str
    fecha_envio: datetime

class Classifier(ABC):
    @abstractmethod
    def classify(self, email: Email) -> Optional[str]:
        """
        Devuelve la categoría asignada al email o None si no clasifica.
        """
        pass

class APIClassifier(Classifier):
    """
    Clasificador por defecto que delega en el endpoint REST de la Parte 1.
    Si la petición falla o el cliente tiene impagos, devuelve None.
    """
    def __init__(self):
        # Carga las variables de entorno desde .env
        load_dotenv()
        self.url = os.getenv("CLASSIFY_URL")
        # Si no está configurada, no clasificamos por defecto
        if not self.url:
            self.url = None

    def classify(self, email: Email) -> Optional[str]:
        if not self.url:
            return None

        payload = {
            "client_id": email.client_id,
            "fecha_envio": email.fecha_envio.strftime("%Y-%m-%d %H:%M:%S"),
            "email_body": email.body
        }

        try:
            resp = requests.post(self.url, json=payload, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            # La API retorna {"exito": bool, "prediccion": str?, "razon": str?}
            if data.get("exito"):
                return data.get("prediccion")
            return None
        except Exception:
            # Impagos, error de red o de servicio -> None
            return None

class ClassifierDeserializer(ABC):
    @abstractmethod
    def deserialize(self, config: dict) -> Classifier:
        """
        Dado un dict con la configuración de reglas, devuelve un Classifier.
        """
        pass

class NaturalLanguageConfigParser(ABC):
    @abstractmethod
    def parse(self, natural_language: str) -> dict:
        """
        Convierte un texto en lenguaje natural a un dict con la configuración:
        {
          "rules": [ {field, op, value, category}, ... ],
          "default": True|False
        }
        """
        pass

class WrappedClassifier:
    """
    Envuelve un parser NL + deserializer para proveer un .classify(email).
    """
    _classifier: Classifier

    def __init__(self,
                 nl_description: str,
                 nl_config_parser: NaturalLanguageConfigParser,
                 classifier_deserializer: ClassifierDeserializer):
        config = nl_config_parser.parse(nl_description)
        self._classifier = classifier_deserializer.deserialize(config)

    def classify(self, email: Email) -> Optional[str]:
        return self._classifier.classify(email)
