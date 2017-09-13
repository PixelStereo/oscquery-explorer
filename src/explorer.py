#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QGroupBox, QListView, QGridLayout, QTreeView, QWidget, QMenu, QMainWindow, QDialog, QVBoxLayout
from PyQt5.QtCore import QTimer, QThread

from zeroconf import ServiceBrowser, Zeroconf
from pyossia.pyqt.device_view import DeviceView
from pyossia import ossia
from inspector import Inspector


class ZeroConfListener(object):
    def __init__(self, *args, **kwargs):
        self.devices_model = args[0]
        self._devices = []

    def remove_service(self, zeroconf, type, name):
        name = name.split('.' + type)[0]
        print('BYE BYE ' + name)
        print('lines', self.devices_model.rowCount())
        for row in range(0, self.devices_model.rowCount()):
            print('truc', self.devices_model.item(row))
            if str(self.devices_model.item(row).node) == name:
                device = self.devices_model.item(row)
                self.devices_model.removeRow(row)
                self._devices.pop(row)
                break
            # TO DO : if we remove the current device, remove its three
        # TODO : SEND A SIGNAL to CLEAR thE tHREE

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = name.split('.' + type)[0]
        port = info.port
        server = info.server
        try:
            target = 'ws://' + server + ':' + str(port)
            device = ossia.OSCQueryDevice("Explorer for " + name, target, 9998)
        except RuntimeError:
            target = 'http://' + server + ':' + str(port)
            device = ossia.OSCQueryDevice("Explorer for " + name, target, 9998)
        # Grab the namespace with an update
        device.update()
        device_item = NodeItem(device)
        self._devices.append(device)
        self.devices_model.appendRow(device_item)
        device_item = DeviceItem(device, device_item)
        print('ADDED ' + str(device))

        
class DeviceItem(QStandardItem):
    """docstring for TreeDevice"""
    def __init__(self, device, parent):
        super(DeviceItem, self).__init__(str(device))
        self._device = None
        self.iterate_children(device.root_node, parent)
        """
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()
        """
        self.device = device
        print('DO IT GUI', self.device)

    def iterate_children(self, node, parent):
        """
        recursive method to explore children until the end
        """
        for nod in node.children():
            child = NodeItem(nod)
            parent.appendRow(child)
            self.iterate_children(nod, child)

    """
    def update(self):
        print('-update')
        self.device.update()
    """

    def update(self):
        self.device.update()

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if device:
            self._device = device

        
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
        self.inspector = Inspector('', model=self.devices_model)
        Layout.addWidget(self.explorer, 0, 0)
        self.device_view = DeviceView(self.devices_model)
        Layout.addWidget(self.device_view, 0, 1)
        Layout.addWidget(self.inspector, 0, 2)
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
                self.inspector.inspect(node)
            elif node.__class__.__name__ == 'OSCQueryDevice':
                #self.device_view.setup(device=node)
                pass
        else:
            print('no node selected')
