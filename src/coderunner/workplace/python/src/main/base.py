# -*- coding: utf-8 -*-
from src.parser.parserfactory import ParserFactory

class Base(object):
    def __init__(self, path):
        self.path = path
        self.factory = ParserFactory()