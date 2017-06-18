# -*- coding: utf-8 -*-
from coderunner.src.utils.inputparser.parserfactory import ParserFactory

class Base(object):
    def __init__(self, path, parser_type):
        self.path = path
        factory = ParserFactory(parser_type)
        self.parser = factory.create(path)
