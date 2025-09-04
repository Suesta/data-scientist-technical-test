from parser import SimpleNLParser
from deserializer import ConfigDeserializer
from base import NaturalLanguageConfigParser, ClassifierDeserializer

def get_nl_config_parser() -> NaturalLanguageConfigParser:
    return SimpleNLParser()

def get_classifier_deserializer() -> ClassifierDeserializer:
    return ConfigDeserializer()
