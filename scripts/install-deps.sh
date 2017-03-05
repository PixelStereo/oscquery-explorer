#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    sudo apt-get -y install python3 python3-setuptools libpython3.5-dev 
    sudo easy_install3 pip
    #sudo apt-get -y install libossia -with-python
  ;;
  osx)
    brew install python3
    brew link --overwrite python3
    #brew install libossia -with-python
  ;;
esac

sudo pip3 install pyinstaller
