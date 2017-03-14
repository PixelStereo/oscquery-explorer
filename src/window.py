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
from inspector import Inspector

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QTreeView, QSlider, QListView, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.Qt import *


class MainWindow(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self):
        super(MainWindow, self).__init__()
        # bound to the embedded test local device
        # it is created when importing pyossia
        self.zero_conf_explorer("oscjson apps")
        self.createTree("Remote Application Viewer")
        self.inspector = Inspector('')
        layout = QGridLayout()
        layout.addWidget(self.zeroconf_group, 0, 0)
        layout.addWidget(self.treeGroup, 0, 1)
        #layout.addWidget(self.controlsGroup, 1, 0)
        layout.addWidget(self.inspector, 0, 2)
        self.setLayout(layout)
        self.setWindowTitle("PyOssia Test App")
        #params = [method for method in dir(the_address) if not method.startswith('__') ]
        #children = the_address.children()
        self.oscquery_device  = None
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

    def node_selection_updated(self):
        """
        called when node selection is updated
        """
        index = self.current_selection_model.selectedIndexes()
        for ind in index:
            node = self.current_model.itemFromIndex(ind)
            if node:
                if node.__class__.__name__ == 'TreeItem':
                    self.inspector.inspect(node.node)
            else:
                self.inspector.clear()

    def device_selection_updated(self, *args, **kwargs):
        """
        called when device selection is updated
        """
        index = self.device_selection_model.selectedIndexes()
        if self.oscquery_device:
            del self.oscquery_device
        for ind in index:
            # create the Remote Device
            try:
                data = ind.data().split('@')
                name = data[0]
                target = data[1].split(':')
                port = int(target[1])
                target = target[0]
                self.current_model.clear()
                oscquery_device = pyossia.ossia.OSCQueryDevice("Explorer for " + name, "http://" + target + ':' + str(port), 9998)
                oscquery_device.update()
                # please make a list of models and check if it already exists
                self.current_model.device = oscquery_device
                self.current_view.selectionModel().selectionChanged.connect(self.node_selection_updated)
                self.current_view.expandAll()
            except():
                print('cannot make connection')

    def zero_conf_explorer(self, name):
        """
        create a zeroconf qgroubbox with a qlist view 
        """
        # create the view
        self.device_view = QListView()
        # add the view to the layout
        # set layout and group
        self.zeroconf_group = QGroupBox(name)
        Layout = QGridLayout()
        self.zeroconf_group.setLayout(Layout)
        self.zeroconf_group.setMinimumWidth(100)
        self.zeroconf_group.setMinimumHeight(300)
        Layout.addWidget(self.device_view, 0, 0)
        # create the model
        self.device_model = QStandardItemModel()
        # link model to the view
        self.device_view.setModel(self.device_model)
        self.device_view.setModel(self.device_model)
        self.device_view.selectionModel().selectionChanged.connect(self.device_selection_updated)
        # set selection
        self.device_selection_model = self.device_view.selectionModel()
        # start zeroconf services
        zeroconf = Zeroconf()
        # start the callback, it will create items
        listener = ZeroConfListener(self.device_model)
        browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", listener)

    def createTree(self, title):
        """
        create the tree
        """
        self.treeGroup = QGroupBox(title)
        self.current_view = QTreeView() 
        self.current_model = TreeModel(None)
        self.current_view.setModel(self.current_model)
        # set selection
        self.current_selection_model = self.current_view.selectionModel()
        self.current_view.expandAll()
        Layout = QGridLayout()
        Layout.addWidget(self.current_view, 0, 0)
        self.treeGroup.setLayout(Layout)
        self.treeGroup.setMinimumWidth(300)
        self.treeGroup.setMinimumHeight(300)
