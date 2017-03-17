#!/bin/sh

set -v

case "$TRAVIS_OS_NAME" in
  linux)
    sudo apt-get -y install python3 python3-setuptools libpython3.6-dev 
    pip install pyqt5
    pip install -v git+https://github.com/PixelStereo/pyossia.git@master
    sudo pip install pyinstaller zeroconf
  ;;
  osx)
    brew install python3
    brew link --overwrite python3
    pip3 install pyqt5
    pip3 install -v git+https://github.com/PixelStereo/pyossia.git@master
    sudo pip3 install pyinstaller zeroconf
  ;;
esac
