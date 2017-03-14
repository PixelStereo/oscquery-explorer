#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
main script
"""
# append ossia_python.so and pyossia module paths
# we will use pip later on
import sys, os
sys.path.append(os.path.abspath('../../libossia/build/'))
sys.path.append(os.path.abspath('../../libossia/OSSIA/ossia-python/'))

from window import MainWindow
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))


if __name__ == "__main__":
    # this is for python2 only
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    app = QApplication(sys.argv)
    try:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except Exception as error:
        print('failed ' + str(error))
    root = QFileInfo(__file__).absolutePath()
    path = root+'/icon/icon.png'
    app.setWindowIcon(QIcon(path))
    mainWin = MainWindow()
    mainWin.show()
    mainWin.setFixedSize(900, 400)
    sys.exit(app.exec_())
    zeroconf.close()