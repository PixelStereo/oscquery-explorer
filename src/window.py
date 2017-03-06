#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main window handles :
- main window
- Menus and all documents-related functions
such as new / open / save / save as…
"""


import os
import sys

import ossia_python as ossia

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QSignalMapper, QPoint, QSize, QSettings, QFileInfo
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMdiArea, \
                            QApplication, QMessageBox, QFileDialog, QWidget

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QCheckBox, QComboBox, QTreeWidgetItem,
        QDial, QGridLayout, QGroupBox, QHBoxLayout, QTreeWidget, QLabel, QScrollBar,
        QSlider, QDoubleSpinBox, QSpinBox, QStackedWidget, QWidget, QLineEdit)


class QLabelSelectable(QLabel):
    """
    QLabel with a selection
    """
    def __init__(self, *args, **kwargs):
        super(QLabelSelectable, self).__init__(*args, **kwargs)

        def mouseReleaseEvent(self, event):
            print "clicked"
        
class MainWindow(QWidget):
    valueChanged = pyqtSignal(int)

    datatypes = {'float':ossia.ValueType.Float, 'int':ossia.ValueType.Int, 'bool':ossia.ValueType.Bool, 'string':ossia.ValueType.String}

    def __init__(self):
        super(MainWindow, self).__init__()
        # create the layout
        self.add_ossia_device("PyOssia Test App")
        self.createTree("Tree")
        self.createControls("Controls")
        self.createInspector("Inspector")
        layout = QHBoxLayout()
        layout.addWidget(self.treeGroup)
        layout.addWidget(self.controlsGroup)
        #layout.addWidget(self.inspectorGroup)
        self.setLayout(layout)
        self.setWindowTitle("PyOssia Test App")
        the_address = self.local_device.find_node('/')
        params = [method for method in dir(the_address) if not method.startswith('__') ]
        children = the_address.children()
        #print(dir(children))
        #print(len(children))
        #print(children.pop_back())

    def add_ossia_device(self, name):
        # create an Ossia Device
        self.local_device = ossia.LocalDevice(name)
        oscquery = self.local_device.create_oscquery_server(3456, 5678)
        if oscquery:
            print('oscquery server started')
        self.add_ossia_parameter('test/value/int')

    def add_ossia_parameter(self, name, datatype='float', domain=None, unique=False, clipmode=None):
        # create the node
        param = self.local_device.add_node(name)
        # create the parameter
        datatype = self.datatypes[datatype]
        param = param.create_address(datatype)
        param.set_bounding_mode(ossia.BoundingMode.Free)
        param.get_domain().set_min(ossia.Value(-1.0))
        param.get_domain().set_max(ossia.Value(1.0))
        def int_handler(value):
            # push a value
            param.push_value(ossia.Value(value))
        # attach a callback function to the boolean address
        #param.add_callback(param.update_model(value.get()))
        return param

    def createTree(self, title):
        self.treeGroup = QGroupBox(title)
        self.tree = QTreeWidget()
        self.tree.header().hide() 
        strings = ['uno', 'dos', 'tres']
        l = []  # list of QTreeWidgetItem to add
        for i in strings:
            l.append(QTreeWidgetItem([i]))  # create QTreeWidgetItem's and append them
        self.tree.addTopLevelItems(l)  # add everything to the tree
        Layout = QGridLayout()
        Layout.addWidget(self.tree, 0, 0)
        self.treeGroup.setLayout(Layout)
        self.treeGroup.setMinimumWidth(300)
        self.treeGroup.setMinimumHeight(300)

    def createControls(self, title):
        self.controlsGroup = QGroupBox(title)
        #self.controlsGroup.setCheckable(True)


        # Create a QGroupBox for each parameter
        # if bool = checkbox
        # if float / int = slider
        # if string = qlineedit + combo

        # int
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

    def createInspector(self, title):
        self.inspectorGroup = QGroupBox(title)
        self.repetitions = QCheckBox("Unique (filter repetitions)")

        self.datatype = QComboBox()
        self.datatype.addItem("Float")
        self.datatype.addItem("Int")
        self.datatype.addItem("String")
        self.datatype.addItem("Impulse")
        self.datatype.addItem("Boolean")
        self.datatype.addItem("Vec3f")
        self.datatype.addItem("Tuple")

        Layout = QGridLayout()
        Layout.addWidget(self.datatype, 0, 0)
        Layout.addWidget(self.repetitions, 0, 4)
        self.inspectorGroup.setLayout(Layout)
        self.inspectorGroup.setMinimumWidth(300)
        self.inspectorGroup.setMinimumHeight(300)
