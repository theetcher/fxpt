try:
    from PySide2 import QtCore, QtGui, QtWidgets
    import shiboken2
except ImportError:
    from PySide import QtCore, QtGui
    QtWidgets = QtGui
    QtCore.QSortFilterProxyModel = QtGui.QSortFilterProxyModel
    try:
        import shiboken as shiboken2
    except ImportError:
        from PySide import shiboken as shiboken2


def isPySide2():
    return int(QtCore.__version__.replace('.', '')[:3]) >= 500
