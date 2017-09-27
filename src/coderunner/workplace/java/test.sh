#!/bin/bash

# set up the working directories
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR=$ROOT_DIR/bin
CLASSPATH=.:$ROOT_DIR/bin

# src and input files' directories
SRC_DIR=$ROOT_DIR/src
INPUT_DIR=$ROOT_DIR/input


opt=$1

echo "Checking required classes..."

$ROOT_DIR/compile.sh 
MAIN_DIR=$SRC_DIR/main


echo "START TEST"
problems=()
cnt=0
if [ "$opt" = "all" ] || [ -z "$opt" ]; then
  for f in $MAIN_DIR/*.java
  do
    ff=${f##*/}
    ff=${ff%.*}
    if [ "$ff" = "Main" ]; then
      continue
    fi
    problems+=("$ff")
  done
else
  problems=($opt)
fi

cnt=0
for problem in ${problems[@]}
do
  echo Run Problem $problem
  cp -f $SRC_DIR/main/$problem.java $SRC_DIR/main/Main.java
  cp -f $SRC_DIR/sols/$problem.java $SRC_DIR/sols/Solution.java
  javac -d $BIN_DIR -cp $CLASSPATH $SRC_DIR/sols/Solution.java
  javac -d $BIN_DIR -cp $CLASSPATH $SRC_DIR/main/Main.java
  echo "========== RESULT =========="
  java -cp $CLASSPATH  main.Main $INPUT_DIR/$problem.txt
  echo "=========== DONE ==========="
  echo
  let cnt=cnt+1
done
echo $cnt problems were run.
