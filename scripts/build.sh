#!/bin/sh

# REMEMBER CURRENT DIR
CURRENT="${PWD##*/}"
# GO ONE DIR UP
cd ../
# DEFAULTVALUE FOR THE APP IS THE NAME OF THE REPO
DEFAULTVALUE="${PWD##*/}"
# GO BACK SRC
cd $CURRENT
# COMMAND LINE ARGUMENT OR REPO NAME
NAME=${1:-$DEFAULTVALUE}
echo "app will be build with the name :" $NAME
pyinstaller --onefile --windowed --icon=icon/icon.icns -n $NAME main.py
