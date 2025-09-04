from typing import Optional, List
from base import Classifier, Email, APIClassifier

class EqualsRuleClassifier(Classifier):
    """
    Clasificador que devuelve una categoría si el campo especificado del email
    es exactamente igual (case-insensitive) al valor dado.
    """
    def __init__(self, field: str, value: str, category: str):
        self.field = field
        # Guardamos el valor en minúsculas para comparaciones case-insensitive
        self.value = value.lower()
        self.category = category

    def classify(self, email: Email) -> Optional[str]:
        # Obtenemos el contenido del campo (subject, body o sender)
        text = getattr(email, self.field, "")
        if text is None:
            return None
        # Comparación exacta en minúsculas
        if text.lower() == self.value:
            return self.category
        return None


class ContainsRuleClassifier(Classifier):
    """
    Clasificador que devuelve una categoría si el campo especificado del email
    contiene (substring, case-insensitive) el valor dado.
    """
    def __init__(self, field: str, value: str, category: str):
        self.field = field
        self.value = value.lower()
        self.category = category

    def classify(self, email: Email) -> Optional[str]:
        text = getattr(email, self.field, "")
        if text is None:
            return None
        # Subcadena en minúsculas
        if self.value in text.lower():
            return self.category
        return None


class SequentialClassifier(Classifier):
    """
    Ensemble de múltiples clasificadores:
      - Aplica cada regla en orden y, al primer resultado no-None, lo devuelve.
      - Si ninguna regla empata:
          * si use_default=True, delega en APIClassifier()
          * si use_default=False, devuelve None.
    """
    def __init__(self, rules: List[Classifier], use_default: bool):
        # Lista de instancias de EqualsRuleClassifier/ContainsRuleClassifier
        self.rules = rules
        # Si queremos llamar al clasificador semántico por defecto, lo instanciamos
        self.default_clf = APIClassifier() if use_default else None

    def classify(self, email: Email) -> Optional[str]:
        # Recorremos cada regla en orden
        for rule in self.rules:
            result = rule.classify(email)
            if result is not None:
                return result
        # Si ninguna regla devolvió algo y hay default_clf, lo llamamos
        if self.default_clf:
            return self.default_clf.classify(email)
        # Si nada, devolvemos None
        return None
