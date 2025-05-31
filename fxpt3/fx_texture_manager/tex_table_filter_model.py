from fxpt3.qt.pyside import QtCore, QtWidgets


class TexTableFilterModel(QtWidgets.QSortFilterProxyModel):

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # if index.column() == 1:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # else:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
