#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main script
"""

import sys
from window import MainWindow
from explorer import ZeroConfListener
from zeroconf import ServiceBrowser, Zeroconf
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
    zeroconf = Zeroconf()
    listener = ZeroConfListener()
    browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", listener)
    mainWin.show()
    sys.exit(app.exec_())
    zeroconf.close()