# -*- coding: utf-8 -*-

from .parser import (
    IntegerParser,
    FloatParser,
    StringParser
)

class ParserFactory(object):
    def __init__(self):
        self.types = {
            'integer': IntegerParser,
            'float': FloatParser,
            'string': StringParser
        }

    def create(self, type_name):
        return self.types[type_name]()