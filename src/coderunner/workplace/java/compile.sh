#!/bin/bash

# set up the working directories
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# bin directory
if [ ! -d "bin" ]; then
    mkdir bin
fi
BIN_DIR=$ROOT_DIR/bin
CLASSPATH=.:$ROOT_DIR/bin

# src and input files' directories
SRC_DIR=$ROOT_DIR/src
INPUT_DIR=$ROOT_DIR/input

arg=$1

if [ "$arg" = 0 ]; then
  exit 0
fi

if [ -z "$ROOT_DIR" -o ! "$ROOT_DIR"=`pwd`  ]; then
  echo "Please resouce set_env.sh"
  exit 0
fi

#collect the item not compiled
function check {
  DIR=$1
  cnt=0
  for fname in $(find $SRC_DIR/$DIR -name '*.java')
  do
    fname="${fname/$SRC_DIR/$BIN_DIR}"
    fname="${fname/.java/.class}"
    if [ ! -f $fname ]; then
      cnt=$(($cnt+1))
    fi
  done
  echo $cnt
}


if [ "$arg" = "objs" ]; then
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/objs -name '*.java')
  exit 0
fi

if [ "$arg" = "utils" ]; then
  ckobjs=$(check "objs")
  if [ ! $ckobjs = 0 ]; then
    javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/objs -name '*.java')
  fi
  javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/utils -name '*.java')
  exit 0
fi


if [ "$arg" = "all" ] || [ -z $arg ]; then
  echo "compile both objs and utils..."
  ckobjs=$(check "objs")
  if [ ! $ckobjs = 0 ]; then
    echo "compile objs..."
    javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/objs -name '*.java')
  else
    echo "objs have been compiled..."
  fi
  ckutils=$(check "utils")
  if [ ! $ckutils = 0 ]; then
    echo "compile utils..."
    javac -d $BIN_DIR -cp $CLASSPATH $(find $SRC_DIR/utils -name '*.java')
  else
    echo "utils have been compiled..."
  fi
  echo "completed..."
  exit 0
fi

