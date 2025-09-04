from base import ClassifierDeserializer
from classifiers import (
    SequentialClassifier,
    EqualsRuleClassifier,
    ContainsRuleClassifier
)

class ConfigDeserializer(ClassifierDeserializer):
    """
    Construye un SequentialClassifier a partir del dict:
      {
        "rules": [ {field, op, value, category}, ... ],
        "default": True|False
      }
    """
    def deserialize(self, config: dict):
        rules = []
        for r in config.get("rules", []):
            field = r["field"]
            value = r["value"]
            category = r["category"]
            if r["op"] == "equals":
                rules.append(EqualsRuleClassifier(field, value, category))
            elif r["op"] == "contains":
                rules.append(ContainsRuleClassifier(field, value, category))
            else:
                raise ValueError(f"Operación desconocida en config: {r['op']}")
        use_default = bool(config.get("default", False))
        return SequentialClassifier(rules, use_default)
