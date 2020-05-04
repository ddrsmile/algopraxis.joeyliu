#!/bin/bash
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR=$ROOT_DIR/src
WORKPLACE=$ROOT_DIR/sample

clang++ -std=c++11 -I $SRC_DIR $WORKPLACE/main.cpp -o $WORKPLACE/main.o
$WORKPLACE/main.o $WORKPLACE/input.txt

rm $WORKPLACE/main.o
