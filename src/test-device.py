#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an example of a device
with I/O communication provided by libossia with pyqt5 GUI
"""

from pyossia import *

import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox


# create the OSSIA Device with the name provided
# here for test purpose
my_device = add_device('PyOssia Device', mode='local')
my_device.expose(protocol='oscquery', udp_port=3456, ws_port=5678)
my_int = my_device.add_param('test/value/int', datatype='int')
my_float = my_device.add_param('test/value/float', datatype='float')
my_bool = my_device.add_param('test/value/bool', datatype='bool')
my_string = my_device.add_param('test/value/string', datatype='string')
my_string.push_value(Value(" Supa String !!"))
my_bool.push_value(Value(True))
my_float.push_value(Value(25.5))
my_int.push_value(Value(50))
my_string.push_value(Value('hello world!'))


class MainWindow(QWidget):
	"""docstring for MainWindow"""
	def __init__(self):
		super(MainWindow, self).__init__()
		# create instrument/module layout
		self.params = QHBoxLayout()
		self.setLayout(self.params)

		#####################################
		# FLOAT
		#####################################
		# Create address GUI / widgets
		self.float_label = QLabel(str(my_float))
		self.my_float_UI = QSlider()
		# Connect to the ossia.Node.Address.Value
		self.my_float_UI.valueChanged.connect(my_float.push)
		self.my_float_UI.valueChanged.connect(my_float.push)
		def my_float_pull(value):
			self.my_float_UI.setValue(value.get())
			self.float_label.setText(str(my_float))
		my_float.add_callback(my_float_pull)
		my_float_pull(my_float.clone_value())
		# Create Address layout
		self.float_layout = QVBoxLayout()
		self.float_group = QGroupBox()
		self.float_group.setFixedSize(80, 120)
		self.float_group.setLayout(self.float_layout)
		self.float_layout.addWidget(self.float_label)
		self.float_layout.addWidget(self.my_float_UI)
		self.params.addWidget(self.float_group, 1)
		#####################################
		# INT
		#####################################
		# Create address GUI / widgets
		self.int_label = QLabel(str(my_int))
		self.my_int_UI = QSlider()
		# Connect to the ossia.Node.Address.Value
		self.my_int_UI.valueChanged.connect(my_int.push)
		self.my_int_UI.valueChanged.connect(my_int.push)
		def my_int_pull(value):
			self.my_int_UI.setValue(value.get())
			self.int_label.setText(str(my_int))
		my_int.add_callback(my_int_pull)
		my_int_pull(my_int.clone_value())
		# Create Address layout
		self.int_layout = QVBoxLayout()
		self.int_group = QGroupBox()
		self.int_group.setFixedSize(80, 120)
		self.int_group.setLayout(self.int_layout)
		self.int_layout.addWidget(self.int_label)
		self.int_layout.addWidget(self.my_int_UI)
		self.params.addWidget(self.int_group, 1)
		#####################################
		# BOOL
		#####################################
		# Create address GUI / widgets
		self.bool_label = QLabel(str(my_bool))
		self.my_bool_UI = QCheckBox()
		# Connect to the ossia.Node.Address.Value
		self.my_bool_UI.stateChanged.connect(my_bool.push)
		self.my_bool_UI.stateChanged.connect(my_bool.push)
		def my_bool_pull(value):
			self.my_bool_UI.setChecked(value.get())
			self.bool_label.setText(str(my_bool))
		my_bool.add_callback(my_bool_pull)
		my_bool_pull(my_bool.clone_value())
		# Create Address layout
		self.bool_layout = QVBoxLayout()
		self.bool_group = QGroupBox()
		self.bool_group.setFixedSize(80, 120)
		self.bool_group.setLayout(self.bool_layout)
		self.bool_layout.addWidget(self.bool_label)
		self.bool_layout.addWidget(self.my_bool_UI)
		self.params.addWidget(self.bool_group, 1)
		#####################################
		# STRING
		#####################################
		# Create address GUI / widgets
		self.string_label = QLabel(str(my_string))
		self.my_string_UI = QLineEdit()
		# Connect to the ossia.Node.Address.Value
		self.my_string_UI.textEdited.connect(my_string.push)
		self.my_string_UI.textEdited.connect(my_string.push)
		def my_string_pull(value):
			self.my_string_UI.setText(value.get())
			self.string_label.setText(str(my_string))
		my_string.add_callback(my_string_pull)
		my_string_pull(my_string.clone_value())
		# Create Address layout
		self.string_layout = QVBoxLayout()
		self.string_group = QGroupBox()
		self.string_group.setFixedSize(400, 120)
		self.string_group.setLayout(self.string_layout)
		self.string_layout.addWidget(self.string_label)
		self.string_layout.addWidget(self.my_string_UI)
		self.params.addWidget(self.string_group, 1)
		self.setFixedSize(720, 160)


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))


if __name__ == "__main__":
    # this is for python2 only
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    app = QApplication(sys.argv)
    try:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except Exception as error:
        print('failed ' + str(error))
    root = QFileInfo(__file__).absolutePath()
    path = root+'/icon/icon.png'
    app.setWindowIcon(QIcon(path))
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    zeroconf.close()