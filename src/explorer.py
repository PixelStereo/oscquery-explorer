#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QGroupBox, QListView, QGridLayout, QTreeView, QWidget, QMenu, QMainWindow, QDialog, QVBoxLayout
from PyQt5.QtCore import QTimer, QThread

from zeroconf import ServiceBrowser, Zeroconf
from pxst_widgets.device_view import DeviceView
from pyossia import ossia
import pyossia
from pxst_widgets.panel import Panel
from inspector import Inspector


class ZeroConfListener(object):
    def __init__(self, *args, **kwargs):
        self.devices_model = args[0]

    def remove_service(self, zeroconf, type, name):
        name = name.split('.' + type)[0]
        print('BYE BYE ' + name)
        for row in range(0, self.devices_model.rowCount()):
            if str(self.devices_model.item(row).name) == name:
                device = self.devices_model.item(row)
                self.devices_model.removeRow(row)
            # TO DO : if we remove the current device, remove its tree
        # TODO : SEND A SIGNAL to CLEAR thE tREE

    def add_service(self, zeroconf, type, name):
        print('Yes, a friend !!')
        info = zeroconf.get_service_info(type, name)
        name = name.split('.' + type)[0]
        port = info.port
        server = info.server
        try:
            target = 'ws://' + server + ':' + str(port)
            device = ossia.OSCQueryDevice("Explorer for " + name, target, 5678)
            print('OK, device ready')
        except RuntimeError:
            print('Exception raised. Is it the best way?')
            target = 'http://' + server + ':' + str(port)
            device = ossia.OSCQueryDevice("Explorer for " + name, target, 5678)
        # Grab the namespace with an update
        print('update it now')
        device.update()
        description = name + ' on ' + server + ':' + str(port)
        device_item = DeviceItem(description, device)
        self.devices_model.appendRow(device_item)
        print('ADDED ' + str(name))

        
class DeviceItem(QStandardItem):
    """docstring for TreeDevice"""
    def __init__(self, description, device):
        super(DeviceItem, self).__init__(description)
        self._device = None
        self.device = device
        device_item = NodeItem(description)
        self.iterate_children(device.root_node, self)
        self.description = description

    def iterate_children(self, node, parent):
        """
        recursive method to explore children until the end
        """
        for nod in node.children():
            child = NodeItem(nod)
            parent.appendRow(child)
            self.iterate_children(nod, child)

    def update(self):
        self.device.update()

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if device:
            self._device = device

    @property
    def node(self):
        return self.device.root_node


    @property
    def name(self):
        return self.description.split(' ')[0]
        
class NodeItem(QStandardItem):
    """
    docstring for TreeItem
    """
    def __init__(self, node):
        nickname = str(node).split('/')[-1]
        super(NodeItem, self).__init__(nickname)
        self.node = node


    @property
    def root_node(self):
        return self.node.root_node

    @property
    def node(self):
        return self._node
    @node.setter
    def node(self, node):
        if node:
            self._node = node

    def update(self):
        self.node.update()

class ZeroConfExplorer(QWidget):
    """
    create a zeroconf qgroubbox with a qlist view 
    """
    def __init__(self, name):
        super(ZeroConfExplorer, self).__init__()
        # init explorer to None
        self.oscquery_device = None
        if not name:
            name = 'OSCJSON thru TCP Explorer'
        # create the view
        self.explorer = QTreeView()
        # Hide Useless Header
        self.explorer.header().hide()
        self.panel = Panel()
        # create right-click menu
        self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.explorer.customContextMenuRequested.connect(self.contextual_menu)
        # create the model
        self.devices_model = QStandardItemModel()
        # link model to the view
        self.explorer.setModel(self.devices_model)
        self.explorer.selectionModel().selectionChanged.connect(self.selection_updated)
        # set selection
        self.device_selection_model = self.explorer.selectionModel()
        # set layout and group
        Layout = QGridLayout()
        # add the view to the layout
        Layout.addWidget(self.explorer, 0, 0)
        Layout.addWidget(self.panel, 0, 1)
        # add the layout to the GroupBox
        self.setLayout(Layout)
        #self.setMinimumSize(300, 300)
        self.explorer.setFixedSize(300, 300)
        # start zeroconf services
        zeroconf = Zeroconf()
        # start the callback, it will create items
        listener = ZeroConfListener(self.devices_model)
        browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", listener)

    def contextual_menu(self, position):
    
        indexes = self.explorer.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
            node = self.devices_model.itemFromIndex(index)
            menu = QMenu()
            if level == 0:
                menu.addAction("Refresh Device Namespace", node.update)
            elif level > 0:
                menu.addAction("Refresh Node", node.update)
            menu.exec_(self.explorer.viewport().mapToGlobal(position))

    def selection_updated(self, *args, **kwargs):
        """
        called when device selection is updated
        we will disconnect our ossia.OSCQueryDevice from the previous device if there was one
        and then we will reconnect it to the current instance of the Device model
        """
        index = self.device_selection_model.selectedIndexes()
        # we consider unique selection
        modelIndex = index[0]
        if modelIndex:
            node = self.devices_model.itemFromIndex(modelIndex).node
            if node.__class__.__name__ == 'Node':
                for param in node.get_parameters():
                    print('---- -Insoect a Parameter- ----', param)
                    self.panel.add_remote(param)
                pass
            elif node.__class__.__name__ == 'OSCQueryDevice':
                print('---- -Insoect a Device- ----')
                #self.device_view.setup(device=node)
        else:
            print('no node selected')
