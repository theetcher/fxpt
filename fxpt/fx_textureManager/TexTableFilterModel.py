from PySide import QtCore, QtGui


class TexTableFilterModel(QtGui.QSortFilterProxyModel):

    def flags(self, index):
        # print 'TexTableFilterModel.flags()'
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
