import re
from base import NaturalLanguageConfigParser

class SimpleNLParser(NaturalLanguageConfigParser):
    """
    Parser que convierte una descripción en lenguaje natural (ES/EN)
    en un dict con la estructura:
    {
      "rules": [
        {"field": ..., "op": "equals"|"contains", "value": ..., "category": ...},
        ...
      ],
      "default": True|False
    }
    """
    # Patrón A: "Si/If (el|the)? campo (contiene|es) “valor”, clasificarlo como “cat”"
    PATTERN_A = re.compile(
        r'(?P<prefix>\b(?:si|if)\b)\s+'                    # "si" o "if"
        r'(?:(?:el|the)\s+)?'                              # opcional "el" o "the"
        r'(?P<field>asunto|subject|cuerpo|body|remitente|sender)\b'
        r'.*?\b(?P<op>contiene|contains|es|is)\b'
        r'[^"“”]*[“"](?P<value>[^"”]+)[”"]'                 # valor entre comillas
        r'.*?(?:clasificarlo\s+como|classify(?:\s+it)?\s+as)\s*[“"](?P<category>[^"”]+)[”"]',
        flags=re.IGNORECASE | re.DOTALL
    )

    # Patrón B (principalmente Español): "asigna la categoría “cat” si (el)? campo (op) “valor”"
    PATTERN_B = re.compile(
        r'asigna(?:\s+la\s+categor(?:[íi]a))?\s*[“"](?P<category>[^"”]+)[”"]'
        r'.*?\b(?:si|if)\b\s+'
        r'(?:(?:el|the)\s+)?'
        r'(?P<field>asunto|subject|cuerpo|body|remitente|sender)\b'
        r'.*?\b(?P<op>contiene|contains|es|is)\b'
        r'[^"“”]*[“"](?P<value>[^"”]+)[”"]',
        flags=re.IGNORECASE | re.DOTALL
    )

    # Detector de default: "usar/usa/use ... clasificador por defecto/default"
    DEFAULT_RE = re.compile(
        r'(?:usar|usa|use)\s+(?:siempre\s+)?(?:el\s+|the\s+)?clasificador\s+(?:por\s+defecto|default)',
        flags=re.IGNORECASE
    )

    FIELD_MAP = {
        "asunto": "subject", "subject": "subject",
        "cuerpo": "body",    "body":    "body",
        "remitente": "sender","sender": "sender"
    }
    OP_MAP = {
        "contiene": "contains", "contains": "contains",
        "es": "equals",         "is": "equals"
    }

    def parse(self, natural_language: str) -> dict:
        text = natural_language
        matches = []

        # Reglas tipo A
        for m in self.PATTERN_A.finditer(text):
            matches.append((
                m.start(),
                m.group('field').lower(),
                m.group('op').lower(),
                m.group('value'),
                m.group('category')
            ))

        # Reglas tipo B
        for m in self.PATTERN_B.finditer(text):
            matches.append((
                m.start(),
                m.group('field').lower(),
                m.group('op').lower(),
                m.group('value'),
                m.group('category')
            ))

        # Ordenamos según aparición en el texto
        matches.sort(key=lambda x: x[0])

        # Construimos la lista de reglas
        rules = []
        for _, raw_field, raw_op, raw_value, raw_cat in matches:
            field = self.FIELD_MAP.get(raw_field, raw_field)
            op    = self.OP_MAP.get(raw_op, raw_op)
            rules.append({
                "field": field,
                "op": op,
                "value": raw_value,
                "category": raw_cat
            })

        # ¿Usar clasificador por defecto?
        use_default = bool(self.DEFAULT_RE.search(text))

        return {"rules": rules, "default": use_default}
