# -*- coding: utf-8 -*-
from .runner import PythonRunner, JavaRunner

runner_mapper = {
    'python': PythonRunner,
    'java': JavaRunner
}

class RunnerNotFound(Exception):
    pass

class RunnerFactory(object):
    def __init__(self, lang_mode=None):
        self.klass = self._get_runner(lang_mode)

    def _get_runner(self, lang_mode=None):
        try:
            return runner_mapper[lang_mode]
        except KeyError:
            raise RunnerNotFound("Unknown Language Mode: {lang_mode}".format(lang_mode=lang_mode))

    def set_klass(self, klass):
        self.klass = klass

    def create(self):
        return self.klass()