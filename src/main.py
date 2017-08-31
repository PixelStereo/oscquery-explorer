#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
main script
"""
import sys

from window import MainWindow
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    # python2 only
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    # end python 2 only
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    zeroconf.close()