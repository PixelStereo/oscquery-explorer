#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

        
class ZeroConfListener(object):
    def __init__(self, *args, **kwargs):
        self.device_model = args[0]

    def remove_service(self, zeroconf, type, name):
        name = name.split('.' + type)[0]
        print('BYE BYE ' + name)
        for row in range(0, self.device_model.rowCount()+1):
            #if self.device.model.item(row).data() == name:
            self.device_model.removeRow(row)
            # TO DO : if we remove the current device, remove its three
        # TODO : SEND A SIGNAL to CLEAR thE tHREE

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = name.split('.' + type)[0]
        port = info.port
        server = info.server
        device = name + '@' + server + ':' + str(port)
        device_item = QStandardItem(device)
        print('ADDED ' + str(device))
        self.device_model.appendRow(device_item)


class TreeItem(QStandardItem):
    """
    docstring for TreeItem
    """
    def __init__(self, node):
        super(TreeItem, self).__init__(str(node).split('/')[-1])
        self._node = None
        self.node = node

    @property
    def node(self):
        return self._node
    @node.setter
    def node(self, node):
        if node:
            self._node = node


class TreeModel(QStandardItemModel):
    """
    docstring for TreeModel
    """
    def __init__(self, root):
        super(TreeModel, self).__init__()
        self._device = None
        self.device = root

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if device:
            self.root = device.get_root_node()
            self.root_item = TreeItem(self.root)
            self._device = device
            self.iterate_children(self.root, self.root_item)
            self.appendRow(self.root_item)

    def iterate_children(self, node, parent):
        """
        recursive method to explore children until the end
        """
        for nod in node.children():
            child = TreeItem(nod)
            parent.appendRow(child)
            self.iterate_children(nod, child)
