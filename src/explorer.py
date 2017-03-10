#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant
from PyQt5.QtCore import Qt

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
		print('ADDED ' + device)
		self.beginInsertRows(QModelIndex(),self.rowCount(), self.rowCount())
		self._devices.append(device)
		self.endInsertRows()
	
	def data(self, index, role=Qt.DisplayRole):
		try:
			device = self._device[index.row()]
		except IndexError:
			return QVariant()
		if role == self.TypeRole:
			return device.name()

		if role == self.SizeRole:
			return device.oscjson_tcp_port()

		return QVariant()

	def roleNames(self):
		return self._roles
