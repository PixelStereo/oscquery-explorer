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
from zeroconf import ServiceBrowser, Zeroconf

import pyossia

from explorer import ZeroConfListener, TreeModel

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QTreeView, QHBoxLayout, QSlider, QListView, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.Qt import *


class ParamUI(QGroupBox):
    """
    Must be subclassed with creation of self.ui (QWidget)
    """
    def __init__(self, param):
        super(ParamUI, self).__init__()
        self.name = str(param)
        self.label = QLabel(self.name)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class FloatUI(ParamUI):
    """docstring for ClassName"""
    def __init__(self, param):
        super(FloatUI, self).__init__()
        self.ui = QSlider()
        self.ui.setMinimum(param.get_domain().get_min().get())
        self.ui.setMaximum(param.get_domain().get_max().get())
        self.layout.addWidget(self.ui)

class Inspector(QGroupBox):
    """docstring for Inspector"""
    def __init__(self, name):
        super(Inspector, self).__init__()
        self.name = name
        self.setEnabled(False)
        self.repetitions = QCheckBox("Unique (filter repetitions)")

        self.datatype = QComboBox()
        self.datatype.addItem("Float")
        self.datatype.addItem("Int")
        self.datatype.addItem("String")
        self.datatype.addItem("Impulse")
        self.datatype.addItem("Boolean")
        self.datatype.addItem("Vec3f")
        self.datatype.addItem("Tuple")
        self.createControls("Controls")
        self.domain = QLineEdit()
        self.bounding_mode = QComboBox()
        self.bounding_mode.addItem('Clip')

        self.id = QLabel()
        self.value = QLabel()
        Layout = QGridLayout()
        Layout.addWidget(self.id, 0, 0)
        Layout.addWidget(self.value, 0, 1)
        Layout.addWidget(self.datatype, 2, 0)
        Layout.addWidget(self.domain, 3, 0)
        Layout.addWidget(self.bounding_mode, 3, 1)
        Layout.addWidget(self.repetitions, 4, 0)
        self.setLayout(Layout)
        #self.setMinimumWidth(300)
        #self.setMinimumHeight(300)

    def inspect(self, node):
        # at this point, we are sure node is a TreeItem
        # is it a node or a param?
        address = node.get_address()
        if 'clone_value' in dir(address):
            self.id.setText(str(node) + ' is a param \n' + str(address.clone_value().get()))
        else:
            self.id.setText(str(node) + ' : is a node')
        #self.value.setText(node.get_address().get())
        self.setEnabled(True)

        




    def createControls(self, title):
        self.controlsGroup = QGroupBox(title)
        #self.controlsGroup.setCheckable(True)


        # Create a QGroupBox for each parameter
        # if bool = checkbox
        # if float / int = slider
        # if string = qlineedit + combo

        # int
        """
        self.an_int_label = QLabelSelectable('/test/value/int')
        self.an_int = QSlider(Qt.Horizontal)
        self.an_int.setFocusPolicy(Qt.StrongFocus)
        self.an_int.setTickPosition(QSlider.TicksBothSides)
        self.an_int.setTickInterval(10)
        self.an_int.setRange(0, 100)
        self.an_int.setSingleStep(1)
        self.an_int_box = QSpinBox()
        self.an_int_box.setRange(0, 100)
        self.an_int_box.valueChanged.connect(self.an_int.setValue)
        #self.an_int_box.valueChanged.connect(int_handler)
        self.an_int.valueChanged.connect(self.an_int_box.setValue)
        #self.an_int.valueChanged.connect(int_handler)


        # float
        def SliderFloatGetter(value):
            scaledValue = self.a_float_box.value()
            scaledValue = scaledValue * 65536
            scaledValue = int(scaledValue)
            self.a_float.setValue(scaledValue)

        def SliderFloatSetter(value):   
            scaledValue = float(value)/65536
            self.a_float_box.setValue(scaledValue)
            # push a value
            float_address.push_value(ossia.Value(scaledValue))

        self.a_float_label = QLabel('/test/value/float')
        self.a_float = QSlider(Qt.Horizontal)
        self.a_float.setRange(0, 65536)
        self.a_float.setFocusPolicy(Qt.StrongFocus)
        self.a_float.setTickPosition(QSlider.TicksBothSides)
        self.a_float.setTickInterval(10)
        #self.a_float.setSingleStep(655.36)
        self.a_float_box = QDoubleSpinBox()
        self.a_float_box.setDecimals(6)
        self.a_float_box.setRange(0, 1)
        self.a_float_box.setSingleStep(0.01)
        self.a_float.valueChanged.connect(SliderFloatSetter)
        self.a_float_box.valueChanged.connect(SliderFloatGetter)
        # create the node
        float_node = self.local_device.add_node("/test/value/float")
        # create the parameter
        float_address = float_node.create_address(ossia.ValueType.Float)

        # attach a callback function to the boolean address
        def float_value_callback(value):
            #self.a_float.setValue(value.get()*100000)
            self.a_float_box.setValue(value.get())

        float_address.add_callback(float_value_callback)
        # push a value
        float_address.push_value(ossia.Value(0.456789))




        # a bool
        self.a_bool_label = QLabel('/test/value/bool')
        self.a_bool = QCheckBox()
        # create the node
        bool_node = self.local_device.add_node("/test/value/bool")
        # create the parameter
        bool_address = bool_node.create_address(ossia.ValueType.Bool)

        # attach a callback function to the boolean address
        def bool_value_callback(value):
            # set the checkbox according to ossia inputs
            self.a_bool.setChecked(value.get())

        bool_address.add_callback(bool_value_callback)
        # push a value
        def bool_handler(value):
            bool_address.push_value(ossia.Value(value))

        self.a_bool.stateChanged.connect(bool_handler)
        bool_address.push_value(ossia.Value(True))
        # a string
        def string_handler(value):
            string_address = string_node.push_value(ossia.Value(value))
        self.a_string_label = QLabel('/test/value/string')
        self.a_string = QLineEdit()
        self.a_string.setText("trap ~± )çà!èàç!67[ÛåÊ’√∏Ô‰ML")
        # create the node
        string_node = self.local_device.add_node("/test/value/string")
        # create the parameter
        string_address = string_node.create_address(ossia.ValueType.String)
        def string_value_callback(value):
            # set the checkbox according to ossia inputs
            self.a_string.setText(value.get())

        string_address.add_callback(string_value_callback)

        # attach a callback function to the boolean address
        def string_value_callback(value):
            self.a_string.setText(value.get())

        string_address.add_callback(string_value_callback)
        # push a value
        string_address.push_value(ossia.Value("trap ~± )çà!èàç!67[ÛåÊ’√∏Ô‰ML"))
        controlsLayout = QGridLayout()
        
        controlsLayout.addWidget(self.an_int_label, 0, 0)
        controlsLayout.addWidget(self.an_int, 0, 1)
        controlsLayout.addWidget(self.an_int_box, 0, 2)
        controlsLayout.addWidget(self.a_float_label, 1, 0)
        controlsLayout.addWidget(self.a_float, 1, 1)
        controlsLayout.addWidget(self.a_float_box, 1, 2)
        controlsLayout.addWidget(self.a_bool_label, 2, 0)
        controlsLayout.addWidget(self.a_bool, 2, 1)
        controlsLayout.addWidget(self.a_string_label, 3, 0)
        controlsLayout.addWidget(self.a_string, 3, 1)
        self.controlsGroup.setLayout(controlsLayout)
        self.controlsGroup.setMinimumWidth(300)
        self.controlsGroup.setMinimumHeight(300)
        """