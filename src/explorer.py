#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QGroupBox, QListView, QGridLayout, QTreeView, QWidget

from zeroconf import ServiceBrowser, Zeroconf
import pyossia
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
        target = 'http://' + server + ':' + str(port)
        device = pyossia.ossia.OSCQueryDevice("Explorer for " + name, target, 9998)
        device_item = TreeItem(name)
        self._devices.append(device)
        self.devices_model.appendRow(device_item)
        device.update()
        device_item = TreeDevice(device, device_item)
        print('ADDED ' + str(device))


class TreeDevice(QStandardItem):
    """docstring for TreeDevice"""
    def __init__(self, device, parent):
        super(TreeDevice, self).__init__()
        self._device = None
        self.iterate_children(device.get_root_node(), parent)

    def iterate_children(self, node, parent):
        """
        recursive method to explore children until the end
        """
        for nod in node.children():
            child = TreeItem(nod)
            parent.appendRow(child)
            self.iterate_children(nod, child)

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if device:
            self._device = device

class TreeItem(QStandardItem):
    """
    docstring for TreeItem
    """
    def __init__(self, node):
        nickname = str(node).split('/')[-1]
        super(TreeItem, self).__init__(nickname)
        self.node = node

    @property
    def node(self):
        return self._node
    @node.setter
    def node(self, node):
        if node:
            self._node = node

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
        self.devices_view = QTreeView()
        # create the model
        self.devices_model = QStandardItemModel()
        # link model to the view
        self.devices_view.setModel(self.devices_model)
        self.devices_view.selectionModel().selectionChanged.connect(self.selection_updated)
        # set selection
        self.device_selection_model = self.devices_view.selectionModel()
        # set layout and group
        self.zeroconf_group = QGroupBox(name)
        Layout = QGridLayout()
        self.zeroconf_group.setLayout(Layout)
        self.zeroconf_group.setMinimumWidth(300)
        self.zeroconf_group.setMinimumHeight(300)
        # add the view to the layout
        Layout.addWidget(self.devices_view, 0, 0)
        self.inspector = Inspector('', model=self.devices_model)
        Layout.addWidget(self.inspector, 0, 1)
        # add the layout to the GroupBox
        self.setLayout(Layout)
        #self.setFixedSize(500, 300)
        # start zeroconf services
        zeroconf = Zeroconf()
        # start the callback, it will create items
        listener = ZeroConfListener(self.devices_model)
        browser = ServiceBrowser(zeroconf, "_oscjson._tcp.local.", listener)

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
            self.inspector.inspect(modelIndex)
        else:
            print('no node selected')
