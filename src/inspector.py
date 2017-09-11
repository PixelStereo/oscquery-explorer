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
from pyossia.pyqt.canvas import add_paramUI

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QTreeView, QHBoxLayout, QSlider, QListView, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.Qt import *


class ParamData(QGroupBox):
    """
    ParamData Class is a GUI that display Properties of a paramerter
    """
    def __init__(self, parameter, **kwargs):
        super(ParamData, self).__init__()
        self.setEnabled(False)
        self.repetitions = QCheckBox("Unique (filter repetitions)")
        self.datatype = QComboBox()
        self.datatype.addItem("Float")
        self.datatype.addItem("Int")
        self.datatype.addItem("String")
        self.datatype.addItem("Impulse")
        self.datatype.addItem("Bool")
        self.datatype.addItem("Vec3f")
        self.datatype.addItem("Tuple")
        self.domain = QLineEdit()
        self.bounding_mode = QComboBox()
        self.bounding_mode.addItem('Clip')
        self.bounding_mode.addItem('Free')
        self.bounding_mode.addItem('Both')
        self.bounding_mode.addItem('Low')
        self.bounding_mode.addItem('High')
        layout = QGridLayout()
        layout.addWidget(QLabel('Datatype'), 2, 0)
        layout.addWidget(self.datatype, 2, 1)
        layout.addWidget(QLabel('Domain'), 3, 0)
        layout.addWidget(self.domain, 3, 1)
        layout.addWidget(QLabel('ClipMode'), 4, 0)
        layout.addWidget(self.bounding_mode, 4, 1)
        layout.addWidget(QLabel('Repetitions'), 5, 0)
        layout.addWidget(self.repetitions, 5, 1)
        self.setLayout(layout)
        self.inspect(parameter)

    def inspect(self, parameter):
        datatype = str(parameter.value_type).split('.')[1]
        self.datatype.setCurrentText(datatype)
        if parameter.domain.min.valid():
            self.domain.setText(str(parameter.domain.min.get()) + ' / ' + str(parameter.domain.max.get()))
        else:
            self.domain.setText('')
        self.repetitions.setChecked(parameter.repetition_filter)
        self.setEnabled(True)


class Inspector(QGroupBox):
    """
    This is a Parameter inspector
    it must refer to a parameter as model in inspect()
    """
    def __init__(self, name, model=None):
        super(Inspector, self).__init__()
        self.paramUI = None
        self.devices_model = model
        self.name = name
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setMaximumSize(330, 400)

    def clearLayout(self):
        """
        Clear Layout / Remove Parameters UI
        """
        if self.layout != None:
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clearLayout(child.layout())

    def inspect(self, modelIndex):
        """
        Inspect a parameter
        """
        item = self.devices_model.itemFromIndex(modelIndex)
        if item.node.__class__.__name__ == 'Node':
            # check if it is a node or a parameter
            if not item.node.parameter:
                # this is a node
                # TODO : explore priority and NODE's attributes
                self.setEnabled(False)
                self.clearLayout()
                self.paramUI = None
                self.paramData = None
            else:
                # this is a parameter
                # remove old widgets
                if self.paramUI:
                    self.clearLayout()
                    self.paramUI = None
                    self.paramData = None
                # create new ones
                self.paramUI = add_paramUI(item.node.parameter)
                self.paramData = ParamData(item.node.parameter)
                self.layout.addWidget(self.paramUI, 0, 0)
                self.layout.addWidget(self.paramData, 2, 0)
                self.setLayout(self.layout)
                self.setEnabled(True)
