#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

class Device(object):

    def __init__(self, name, oscjson_tcp_port):
        self._name = name
        self._oscjson_tcp_port = oscjson_tcp_port

    def __repr__(self):
        return(self.name + ' on port ' + self.oscjson_tcp_port)
    @property
    def name(self):
        return self._name
    @property
    def oscjson_tcp_port(self):
        return self._oscjson_tcp_port

class DeviceModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    OscJsonTcpRole = Qt.UserRole + 2
    _roles = {NameRole: "name", OscJsonTcpRole: "oscjson_tcp_port"}
    def __init__(self):
        super(DeviceModel, self).__init__()
        self.root_item = QStandardItem('root stuff')
        self._devices = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._devices)

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = info.properties['Description']
        port = info.properties['LocalPort']
        print('Bye Bye ' + name + ' on tcp port ' + port)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = info.properties['Description']
        port = info.properties['LocalPort']
        device = Device(name, port)
        print('--------------------')
        print('--------------------')
        print('ADDED ' + str(device))
        print('--------------------')
        device_item = QStandardItem(str(device))
        self.appendRow(self.root_item)
        #self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        #self._devices.append(device)
        #self.endInsertRows()
        #self.setData(QModelIndex(), device)
        print(self.index(0).data(self.NameRole))

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            self._devices[row] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def data(self, index, role=Qt.DisplayRole):
        try:
            device = self._devices[index.row()]
        except IndexError:
            return QVariant()
        if role == Qt.DisplayRole:
            return str(device)
        if role == self.NameRole:
            return device.name

        if role == self.OscJsonTcpRole:
            return device.oscjson_tcp_port

        return QVariant()

    def roleNames(self):
        return self._roles
