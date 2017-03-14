#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main window handles :
- main window
- Menus and all documents-related functions
such as new / open / save / save as…
"""


import os
import sys

import pyossia

from explorer import ZeroConfExplorer

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QTreeView, QSlider, QListView, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.Qt import *


class MainWindow(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self):
        super(MainWindow, self).__init__()
        # create a ZeroConf Explorer
        self.explorer = ZeroConfExplorer("oscjson apps")
        layout = QGridLayout()
        layout.addWidget(self.explorer, 0, 0)
        self.setLayout(layout)
        self.setWindowTitle("PyOssia Test App")
        #params = [method for method in dir(the_address) if not method.startswith('__') ]
        #children = the_address.children()
        #print(dir(children))
        #print(len(children))
        #print(children.pop_back())
        self.readSettings()

    def closeEvent(self, closevent):
        """
        method called when the main window wants to be closed
        """
        self.writeSettings()
        closevent.accept()

    def readSettings(self):
        """
        read the settings
        """
        settings = QSettings('pixel-stereo', 'lekture')
        pos = settings.value('pos')
        size = settings.value('size')
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        """
        write settings
        """
        settings = QSettings('Pixel Stereo', 'pyossia-test-app')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

