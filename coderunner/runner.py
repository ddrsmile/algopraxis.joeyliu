# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import string, random
from coderunner import BASE_DIR

WORKPLACE = os.path.join(BASE_DIR, 'workplace')


class CustomRuntimeError(Exception):
    pass


class Runner(object):
    def __init__(self):
        self.workplace_name = self._generate_workplace_name()
        self.workplace = None

    def _generate_workplace_name(self):
        workplace_name = ''
        while not workplace_name and os.path.isdir(os.path.join(WORKPLACE, workplace_name)):
            workplace_name = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(10)])
        return workplace_name

    def _rearrange_error_messages(self, estr):
        return estr

    def str2list(self, strs):
        return strs.decode('utf-8').strip().split('\n')

    def _set_files(self, main, sol, testcase):
        raise NotImplementedError()

    def perform_run(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self, main, sol, testcase, *args, **kwargs):
        self._set_files(main, sol, testcase)

        try:
            return self.perform_run(*args, **kwargs)
        except CustomRuntimeError as e:
            massage = self._rearrange_error_messages(str(e))
            return [massage]
        except Exception as e:
            message = "An exception of type {0} occurred.\n {1}"
            return [message.format(type(e).__name__, str(e))]
        finally:
            if self.workplace and os.path.isdir(self.workplace):
                shutil.rmtree(self.workplace)

class PythonRunner(Runner):
    def __init__(self):
        super(PythonRunner, self).__init__()
        self.workplace = os.path.join(WORKPLACE, 'python', self.workplace_name)

    def _rearrange_error_messages(self, estr):
        lines = estr.strip().split('\n')[-3:]
        items = []
        items.append(lines[0].split(',')[1].strip())
        items.append(lines[-1].strip())
        return ", ".join(items)

    def _set_files(self, main, sol, testcase):
        os.mkdir(self.workplace)
        open(os.path.join(self.workplace, '__init__.py'), 'a').close()

        with open(os.path.join(self.workplace, 'main.py'), 'w') as f:
            for line in main:
                f.write(line)

        with open(os.path.join(self.workplace, 'sol.py'), 'w') as f:
            for line in sol:
                f.write(line)

        with open(os.path.join(self.workplace, 'input.txt'), 'w') as f:
            for line in testcase:
                f.write(line)

    def perform_run(self):
        cmds = [os.path.join(BASE_DIR, 'workplace/python/run.py'), '-w', self.workplace_name]
        result = subprocess.run(cmds,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        if result.returncode and result.stderr:
            raise CustomRuntimeError(str(result.stderr.decode('utf-8')))

        return self.str2list(result.stdout)

class JavaRunner(Runner):
    def __init__(self):
        super(JavaRunner, self).__init__()
        self.workplace = os.path.join(WORKPLACE, 'java', self.workplace_name)

    def _rearrange_error_messages(self, estr):
        lines = estr.strip().split('\n')[:4]
        items = []
        items.append('line ' + lines[0].split(':', 1)[1].strip())
        items.append(lines[3].split(':')[1].strip())
        return ', '.join(items)

    def _set_files(self, main, sol, testcase):
        os.mkdir(self.workplace)

        with open(os.path.join(self.workplace, 'Main.java'), 'w') as f:
            # add required packages
            f.write('import auxiliary.*;')
            f.write('import parser.*;')
            f.write('import java.util.*;')
            f.write('import java.io.*;')
            for line in main:
                f.write(line)

        with open(os.path.join(self.workplace, 'Solution.java'), 'w') as f:
            # add required packages
            f.write('import java.util.*;')
            for line in sol:
                f.write(line)

        with open(os.path.join(self.workplace, 'input.txt'), 'w') as f:
            for line in testcase:
                f.write(line)

    def perform_run(self):
        main_path = os.path.join(self.workplace, 'Main.java')
        sol_path = os.path.join(self.workplace, 'Solution.java')
        input_path = os.path.join(self.workplace, 'input.txt')
        class_path = ':'.join([os.path.join(BASE_DIR, 'workplace', 'java', 'bin'), self.workplace])

        c_cmds = ['javac', '-d', self.workplace, '-cp', class_path, main_path, sol_path]
        r_cmds = ['java', '-cp', class_path, 'Main', input_path]

        c_result = subprocess.run(c_cmds,
                                  stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if c_result.returncode and c_result.stderr:
            raise CustomRuntimeError(str(c_result.stderr.decode('utf-8')))

        r_result = subprocess.run(r_cmds,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        if r_result.returncode and r_result.stderr:
            raise CustomRuntimeError(str(c_result.stderr.decode('utf-8')))

        return self.str2list(r_result.stdout)

class CppRunner(Runner):
    def __init__(self):
        super(CppRunner, self).__init__()
        self.workplace = os.path.join(WORKPLACE, 'c_cpp', self.workplace_name)

    def _rearrange_error_messages(self, estr):
        lines = estr.strip().split('\n')[:3]
        items = []
        if 'Solution' in lines[0]:
            info = lines[0].split(':')
            items.append('line ' + str(int(info[1].strip()) - 1))
            items.append(info[3].strip() + ': ' + info[4].strip())
        else:
            info = lines[1].split(':')
            items.append('line ' + str(int(info[1].strip()) - 1))
            items.append(info[3].strip() + ': ' + info[4].strip())
            items.append(lines[2].strip())
        return ', '.join(items)

    def _set_files(self, main, sol, testcase):
        os.mkdir(self.workplace)

        with open(os.path.join(self.workplace, 'main.cpp'), 'w') as f:
            for line in main:
                f.write(line)

        with open(os.path.join(self.workplace, 'sols.cpp'), 'w') as f:
            f.write('#include "sols.h"\n')
            for line in sol:
                f.write(line)

        with open(os.path.join(self.workplace, 'input.txt'), 'w') as f:
            for line in testcase:
                f.write(line)

    def perform_run(self):
        main_path = os.path.join(self.workplace, 'main.cpp')
        o_path = os.path.join(self.workplace, 'main.o')
        input_path = os.path.join(self.workplace, 'input.txt')

        include_path = os.path.join(WORKPLACE, 'c_cpp', 'include')
        parser_include_path = os.path.join(WORKPLACE, 'c_cpp', 'parser/include')
        parser_lib_path = os.path.join(WORKPLACE, 'c_cpp', 'parser/lib')

        c_cmds = ['clang++', '-std=c++11', '-I', include_path, '-o', o_path, main_path, '-I', parser_include_path, '-L', parser_lib_path, '-lparser',]
        r_cmds = [o_path, input_path]

        c_result = subprocess.run(c_cmds,
                                  stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if c_result.returncode and c_result.stderr:
            raise CustomRuntimeError(str(c_result.stderr.decode('utf-8')))

        r_result = subprocess.run(r_cmds,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        if r_result.returncode and r_result.stderr:
            raise CustomRuntimeError(str(c_result.stderr.decode('utf-8')))

        return self.str2list(r_result.stdout)