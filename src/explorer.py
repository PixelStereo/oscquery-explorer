#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

        
class ZeroConfListener(object):
    def __init__(self, *args, **kwargs):
        print(args[0])
        self.device_model = args[0]

    def remove_service(self, zeroconf, type, name):
        name = name.split('.' + type)[0]
        print('BYE BYE ' + name)
        for row in range(0, self.device_model.rowCount()+1):
            print(row, name, self.device_model.match(row))
            if self.device_model.data(QModelIndex(), row) == name:
                self.device_model.removeRow(row)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        name = name.split('.' + type)[0]
        port = info.port
        device = name + ':' + str(port)
        device_item = QStandardItem(name)
        print('ADDED ' + str(device))
        self.device_model.appendRow(device_item)
