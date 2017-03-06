#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        main_layout = QtWidgets.QVBoxLayout()

        # Create the model
        self.model = MyModel()

        # Create a slider and link it to the model
        self.slider1 = QtWidgets.QSlider()
        self.model.add_slider(self.slider1)        
        main_layout.addWidget(self.slider1)

        # Add a lineEdit and button to force update the model
        # Note that the LineEdit is not linked to the model, so won't update with the slider
        self.edit = QtWidgets.QLineEdit()
        button = QtWidgets.QPushButton('update model')
        button.clicked.connect(self.on_clicked)        
        main_layout.addWidget(self.edit)
        main_layout.addWidget(button)

        self.setLayout(main_layout)

    def on_clicked(self):
        self.model.update_model(int(self.edit.text()),self.slider1)

class MyModel(QtGui.QStandardItemModel):
    def __init__(self,*args,**kwargs):
        super(MyModel,self).__init__(*args,**kwargs)
        self._slider_list = {}
        self.itemChanged.connect(self.on_item_changed)

    def add_slider(self,slider):
        if slider in self._slider_list:
            raise Exception('You cannot link a slider to the model twice')

        item = QtGui.QStandardItem(str(slider.value()))
        self._slider_list[slider] = item
        self.appendRow(item)
        slider.valueChanged.connect(lambda value: self.update_model(value,slider))

    def update_model(self,value,slider):
        if str(value) != self._slider_list[slider].text():
            self._slider_list[slider].setText(str(value))
            print 'update_model: %d'%value

    def on_item_changed(self,item):
        slider = self._slider_list.keys()[self._slider_list.values().index(item)]
        if slider.value() != int(item.text()):
            slider.setValue(int(item.text()))
            print 'on_item_changed: %s'%item.text()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())