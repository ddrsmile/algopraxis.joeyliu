# -*- coding: utf-8 -*-

class ParserFactory(object):
    def __init__(self, type=None):
        self.type = type

    def set_type(self, type):
        self.type =type

    def create(self, input_path=None):
        return self.type(input_path)