#!/bin/bash

# set up the working directories
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

BIN_DIR=$ROOT_DIR/bin
CLASSPATH=.:$ROOT_DIR/bin


javac -d $BIN_DIR -cp $CLASSPATH $ROOT_DIR/sample/Main.java $ROOT_DIR/sample/Solution.java
java -cp $CLASSPATH  Main $ROOT_DIR/sample/input.txt
