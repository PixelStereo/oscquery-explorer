#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class ZeroConfListener(object):
    def __init__(self, *args, **kwargs):
        print(args[0])
        self.device_model = args[0]

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        #name = info.properties['Description']
        #port = info.properties['LocalPort']
        print('Bye Bye ' + name )

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        #name = info.properties['Description']
        #port = info.properties['LocalPort']
        device = name.split('._oscjson')[0]
        device = QStandardItem(device)
        device.setCheckable(True)
        print('ADDED ' + str(device), str(self.device_model))
        self.device_model.appendRow(device)
