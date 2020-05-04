#!/bin/bash

# set up the working directories
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# bin directory
if [ ! -d "bin" ]; then
    mkdir bin
fi
BIN_DIR=$ROOT_DIR/bin
CLASSPATH=.:$ROOT_DIR/bin

# src directories
SRC_DIR=$ROOT_DIR/src

arg=$1

if [ "$arg" = 0 ]; then
  exit 0
fi


if [ "$arg" = "aux" ]; then
  echo "compile auxiliary..."
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/auxiliary -name '*.java')
  echo "completed..."
  exit 0
fi

if [ "$arg" = "parser" ]; then
  echo "compile parser..."
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/parser -name '*.java')
  echo "completed..."
  exit 0
fi

if [ "$arg" = "all" ] || [ -z $arg ]; then
  echo "compile both auxiliary and parser..."
  echo "compile auxiliary..."
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/auxiliary -name '*.java')
  echo "compile parser..."
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/parser -name '*.java')
  echo "completed..."
  exit 0
fi

