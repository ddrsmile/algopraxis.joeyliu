# -*- coding: utf-8 -*-
import os
import sys
import importlib
import shutil
import string, random
from coderunner import BASE_DIR
WORKPLACE = os.path.join(BASE_DIR, 'workplace')

class Runner:
    def __init__(self):
        self.work_dir = self.create_tmep_work_dir()

    def create_tmep_work_dir(self):
        work_dir=''
        while not work_dir and os.path.isdir(os.path.join(WORKPLACE, work_dir)):
            work_dir = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(10)])
        return work_dir

    def set_files(self, main_content, sol_content, input_data):
        work_dir = os.path.join(WORKPLACE, self.work_dir)
        os.mkdir(work_dir)

        open(os.path.join(work_dir, '__init__.py'), 'a').close()

        with open(os.path.join(work_dir, 'main.py'), 'w') as f:
            for line in main_content:
                f.write(line)

        with open(os.path.join(work_dir, 'sol.py'), 'w') as f:
            for line in sol_content:
                f.write(line)

        with open(os.path.join(work_dir, 'input.txt'), 'w') as f:
            for line in input_data:
                f.write(line)

    def unload(self):
        loaded_modules = [
            'coderunner.src.main',
            'coderunner.src.main.base',
            'coderunner.src.sols.sol',
            'coderunner.src.utils.inputparser',
            'coderunner.src.utils.inputparser.parserfactory',
            'coderunner.src.utils.inputparser.parser',
            'coderunner.workplace.{work_dir}.main'.format(work_dir=self.work_dir),
            'coderunner.workplace.{work_dir}.sol'.format(work_dir=self.work_dir)
        ]
        for module in loaded_modules:
            try:
                del sys.modules[module]
            except KeyError:
                pass


    def run(self):
        try:
            main = importlib.import_module('coderunner.workplace.{work_dir}.main'.format(work_dir=self.work_dir))
            m = main.Main(os.path.join(WORKPLACE, self.work_dir, 'input.txt'))
            output = m.main()
            return output
        except Exception as e:
            message = "An exception of type {0} occurred. Arguments:\n{1!r}"
            return [message.format(type(e).__name__, str(e))]
        finally:
            self.unload()
            shutil.rmtree(os.path.join(WORKPLACE, self.work_dir))


