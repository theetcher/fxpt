try:
    from PySide6 import QtCore
    from PySide6 import QtGui
    from PySide6 import QtWidgets
    from PySide6 import QtUiTools
    import shiboken6 as shiboken

except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
    from PySide2 import QtUiTools
    import shiboken2 as shiboken

    QtGui.QActionGroup = QtWidgets.QActionGroup
    QtGui.QAction = QtWidgets.QAction



# def isPySide2():
#     return int(QtCore.__version__.replace('.', '')[:3]) >= 500
