from PyQt5 import QtCore
from PyQt5 import QtWidgets

class ListMOdel(QtCore.QAbstractListModel):
    def __init__(self , data=[] ,parent=None):
        QtCore.QAbstractListModel.__init__(self,parent)
        self.__data=data

    def rowCount(self ,parent):
        return len(self.__data)

    def data(self,index,role):

        if role == QtCore.Qt.DisplayRole:
            row=index.row()
            value = self.__data[row]
            return value

    def flags(self,index):
        return QtCore.Qt.ItemIsEditable |QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsSelectable

    def setData(self,index,value,role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row= index.row()
            self.__data[row]=value
            return True
        return False

class MainWin(QtWidgets.QMainWindow):
    itemName = ""
    def __init__(self, inheritance=None):
        super(MainWin, self).__init__()
        self.ui=uic.loadUi("MainWin.ui", self)

        self.wordList = FileProc.WordStorage().readWordFile()

        self.showListView()
        self.itemName = ""

    def showListView(self, file = 'wordlist.db'):
        MainWin.wordList = FileProc.WordStorage().readWordFile(file)
        data=[]
        for row in MainWin.wordList:
            data.append(row)

        model = ListMOdel(data)
        self.listView.setModel(model)
