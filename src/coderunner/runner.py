# -*- coding: utf-8 -*-
import os
import sys
import importlib
import shutil
from subprocess import check_call, Popen, PIPE
from subprocess import CalledProcessError
import string, random
from coderunner import BASE_DIR
WORKPLACE = os.path.join(BASE_DIR, 'workplace')

commands = {
    'python' : [os.path.join(BASE_DIR, 'workplace/python/run.py'), '-w'],
    'java': [],
    'c_cpp': []
}

class Runner(object):
    def __init__(self):
        self.work_dir = self.create_tmep_work_dir()

    def create_tmep_work_dir(self):
        work_dir=''
        while not work_dir and os.path.isdir(os.path.join(WORKPLACE, work_dir)):
            work_dir = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(10)])
        return work_dir

    def str2list(self, strs):
        strs = strs.split(b'\n')
        outputs = []
        for s in strs:
            if s:
                outputs.append(s.decode('utf-8'))
        return outputs

    def set_files(self, *args, **kwargs):
        raise NotImplementedError()

    def run(self, *args, **kwargs):
        raise NotImplementedError()

class PythonRunner(Runner):
    def __init__(self):
        super(PythonRunner, self).__init__()

    def set_files(self, main, sol, testcase):
        work_dir = os.path.join(WORKPLACE, 'python', self.work_dir)
        os.mkdir(work_dir)

        open(os.path.join(work_dir, '__init__.py'), 'a').close()

        with open(os.path.join(work_dir, 'main.py'), 'w') as f:
            for line in main:
                f.write(line)

        with open(os.path.join(work_dir, 'sol.py'), 'w') as f:
            for line in sol:
                f.write(line)

        with open(os.path.join(work_dir, 'input.txt'), 'w') as f:
            for line in testcase:
                f.write(line)

    def run(self):
        #try:
        #    main = importlib.import_module('coderunner.workplace.python.{work_dir}.main'.format(work_dir=self.work_dir))
        #    m = main.Main(os.path.join(WORKPLACE, 'python', self.work_dir, 'input.txt'))
        #    output = m.main()
        #    return output
        #except Exception as e:
        #    message = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #    return [message.format(type(e).__name__, str(e))]
        #finally:
        #    self.unload()
        #    shutil.rmtree(os.path.join(WORKPLACE, 'python', self.work_dir))

        cmds = [os.path.join(BASE_DIR, 'workplace/python/run.py'), '-w', self.work_dir]

        p = Popen(cmds,  stdin =  PIPE,stdout = PIPE, stderr = PIPE )
        stdout, stderr = p.communicate()
        outputs = self.str2list(stdout)
        shutil.rmtree(os.path.join(WORKPLACE, 'python', self.work_dir))
        return outputs

class JavaRunner(Runner):
    def __init__(self):
        super(JavaRunner, self).__init__()

    def set_files(self, main, sol, testcase):
        work_dir = os.path.join(WORKPLACE, 'java', self.work_dir)
        os.mkdir(work_dir)

        with open(os.path.join(work_dir, 'Main.java'), 'w') as f:
            for line in main:
                f.write(line)

        with open(os.path.join(work_dir, 'Solution.java'), 'w') as f:
            f.write('import java.util.*;\n')
            for line in sol:
                f.write(line)

        with open(os.path.join(work_dir, 'input.txt'), 'w') as f:
            for line in testcase:
                f.write(line)

    def run(self):
        work_path = os.path.join(BASE_DIR, 'workplace', 'java', self.work_dir)
        main_path = os.path.join(work_path, 'Main.java')
        sol_path = os.path.join(work_path, 'Solution.java')
        input_path = os.path.join(work_path, 'input.txt')
        class_path = ':'.join([os.path.join(BASE_DIR, 'workplace', 'java', 'bin'), work_path])

        ccmds = ['javac', '-d', work_path, '-cp', class_path, main_path, sol_path]
        rcmds = ['java', '-cp', class_path, 'Main', input_path]

        try:
            check_call(ccmds)
        except CalledProcessError:
            return None

        p = Popen(rcmds, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        outputs = self.str2list(stdout)
        shutil.rmtree(os.path.join(WORKPLACE, 'java', self.work_dir))
        return outputs

def run(lang_mode, main, sol, testcase):
    if lang_mode == 'python':
        runner = PythonRunner()
    elif lang_mode == 'java':
        runner = JavaRunner()
    else:
        return ["unknow language mode!!"]
    runner.set_files(main, sol, testcase)
    outputs = runner.run()
    return outputs