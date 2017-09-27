#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import importlib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

unload_modules = [
    'src.main.main',
    'src.main',
    'src.main.base',
    'src.sols.sol',
    'src.sols',
    'src.utils.inputparser',
    'src.utils.inputparser.parserfactory',
    'src.utils.inputparser.parser'
]

def run(work_dir):
    main = importlib.import_module('{work_dir}.main'.format(work_dir=work_dir))
    input_path = os.path.join(CURRENT_DIR, work_dir, 'input.txt')
    m = main.Main(input_path)
    output = m.main()
    return output


def unload():
    for module in unload_modules:
        try:
            del sys.modules[module]
        except KeyError:
            pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="run submitted python code")
    parser.add_argument("-w", "--workplace", help="workplace name where submitted codes are")
    args = parser.parse_args()
    results = run(args.workplace)
    for result in results:
        print(result)