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
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QHBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox


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
my_float.push_value(Value(2.22))
my_int.push_value(Value(222))
my_string.push_value(Value('hello world!'))
print(1)


class MainWindow(QWidget):
	"""docstring for MainWindow"""
	def __init__(self):
		super(MainWindow, self).__init__()
		self.params = QHBoxLayout()
		self.setLayout(self.params)
		self.float_label = QLabel('float')
		self.params.addWidget(self.float_label, 0)
		self.my_float_UI = QSlider()
		self.params.addWidget(self.my_float_UI, 1)
		self.my_float_UI.valueChanged.connect(my_float.push)
		def float_pull(value):
			self.my_float_UI.setValue(value.get())
		my_float.add_callback(float_pull)
		self.int_label = QLabel('int')
		self.params.addWidget(self.int_label, 6)
		self.my_int_UI = QSlider()
		self.params.addWidget(self.my_int_UI, 7)
		self.my_int_UI.valueChanged.connect(my_int.push)
		def int_pull(value):
			self.my_int_UI.setValue(value.get())
		my_int.pull(int_pull)
		self.string_label = QLabel('string')
		self.params.addWidget(self.string_label, 6)
		self.my_string_UI = QLineEdit()
		self.params.addWidget(self.my_string_UI, 7)
		self.my_string_UI.textEdited.connect(my_string.push)
		def string_pull(value):
			self.my_string_UI.setText(str(value.get()))
		my_string.pull(string_pull)
		self.bool_label = QLabel('bool')
		self.params.addWidget(self.bool_label, 6)
		self.my_bool_UI = QCheckBox()
		self.params.addWidget(self.my_bool_UI, 7)
		self.my_bool_UI.stateChanged.connect(my_bool.push)
		def bool_pull(value):
			self.my_bool_UI.setChecked(value.get())
		my_bool.pull(bool_pull)

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