#!/bin/bash

# set up the working directories
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR=$ROOT_DIR/bin
CLASSPATH=.:$ROOT_DIR/bin

# src and input files' directories
SRC_DIR=$ROOT_DIR/src
INPUT_DIR=$ROOT_DIR/input

num=$1

cp -f $SRC_DIR/main/$num.java $SRC_DIR/main/Main.java
cp -f $SRC_DIR/sols/$num.java $SRC_DIR/sols/Solution.java
javac -d $BIN_DIR -cp $CLASSPATH $SRC_DIR/sols/Solution.java
javac -d $BIN_DIR -cp $CLASSPATH $SRC_DIR/main/Main.java
java -cp $CLASSPATH  main.Main $INPUT_DIR/$num.txt
