try:
    import PyQt4 as _PyQt4
except ImportError:
    _PyQt4 = None

try:
    import PySide as _PySide
except ImportError:
    _PySide = None

from PSTypes import UITypes
from com import message


# noinspection PyAttributeOutsideInit
class QtCtrlBase(object):

    def __init__(self, qt, control, defaultValue):
        self.qt = qt
        self.control = control
        self.controlName = str(control.objectName())
        self.defaultValue = defaultValue

    def ctrl2Dict(self, prefDict):
        raise NotImplementedError('Call to abstract method.')

    def dict2Ctrl(self, prefDict):
        raise NotImplementedError('Call to abstract method.')


class QtCtrlWindow(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlWindow, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName + 'X'] = self.control.x()
        prefDict[self.controlName + 'Y'] = self.control.y()
        prefDict[self.controlName + 'Width'] = self.control.width()
        prefDict[self.controlName + 'Height'] = self.control.height()

    def dict2Ctrl(self, prefDict):
        x = prefDict[self.controlName + 'X'] if self.controlName + 'X' in prefDict else self.defaultValue[0]
        y = prefDict[self.controlName + 'Y'] if self.controlName + 'Y' in prefDict else self.defaultValue[1]
        width = prefDict[self.controlName + 'Width'] if self.controlName + 'Width' in prefDict else self.defaultValue[2]
        height = prefDict[self.controlName + 'Height'] if self.controlName + 'Height' in prefDict else self.defaultValue[3]
        self.control.move(x, y)
        self.control.resize(width, height)



constructors = {
    UITypes.PYQTWindow: QtCtrlWindow,
    UITypes.PYQTLineEdit: QtCtrlBase,
    UITypes.PYQTCheckBox: QtCtrlBase,
    UITypes.PYQTCheckBoxTri: QtCtrlBase,
    UITypes.PYQTRadioButton: QtCtrlBase,
    UITypes.PYQTCheckButton: QtCtrlBase,
    UITypes.PYQTComboBox: QtCtrlBase,
    UITypes.PYQTComboBoxNoEdit: QtCtrlBase,
    UITypes.PYQTTabControl: QtCtrlBase,
    UITypes.PYQTSplitter: QtCtrlBase,
    UITypes.PYQTListWidget: QtCtrlBase,
    UITypes.PYQTTreeWidget: QtCtrlBase,
    UITypes.PYQTTableWidget: QtCtrlBase,
    UITypes.PYQTListView: QtCtrlBase,
    UITypes.PYQTTreeView: QtCtrlBase,
    UITypes.PYQTTableView: QtCtrlBase,
    UITypes.PYQTColumnView: QtCtrlBase,

    UITypes.PYSIDEWindow: QtCtrlWindow,
    UITypes.PYSIDELineEdit: QtCtrlBase,
    UITypes.PYSIDECheckBox: QtCtrlBase,
    UITypes.PYSIDECheckBoxTri: QtCtrlBase,
    UITypes.PYSIDERadioButton: QtCtrlBase,
    UITypes.PYSIDECheckButton: QtCtrlBase,
    UITypes.PYSIDEComboBox: QtCtrlBase,
    UITypes.PYSIDEComboBoxNoEdit: QtCtrlBase,
    UITypes.PYSIDETabControl: QtCtrlBase,
    UITypes.PYSIDESplitter: QtCtrlBase,
    UITypes.PYSIDEListWidget: QtCtrlBase,
    UITypes.PYSIDETreeWidget: QtCtrlBase,
    UITypes.PYSIDETableWidget: QtCtrlBase,
    UITypes.PYSIDEListView: QtCtrlBase,
    UITypes.PYSIDETreeView: QtCtrlBase,
    UITypes.PYSIDETableView: QtCtrlBase,
    UITypes.PYSIDEColumnView: QtCtrlBase,
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UITypes.TypesPYQT:
        if _PyQt4:
            return constructors[uiType](_PyQt4, control, defaultValue)
        else:
            message('Cannot create controller: PyQt is not available.')
            return

    if uiType in UITypes.TypesPYSIDE:
        if _PySide:
            return constructors[uiType](_PySide, control, defaultValue)
        else:
            message('Cannot create controller: PySide is not available.')
            return

