try:
    import PyQt4 as _PyQt4
except ImportError:
    _PyQt4 = None

try:
    import PySide as _PySide
except ImportError:
    _PySide = None

from UITypes import UITypes
from com import message


# noinspection PyAttributeOutsideInit
class QtControllerBase(object):

    def __init__(self, qt, control, defaultValue,):
        self.qt = qt
        self.control = control
        self.defaultValue = defaultValue


constructors = {
    UITypes.PYQTWindow: QtControllerBase,
    UITypes.PYQTLineEdit: QtControllerBase,
    UITypes.PYQTCheckBox: QtControllerBase,
    UITypes.PYQTCheckBoxTri: QtControllerBase,
    UITypes.PYQTRadioButton: QtControllerBase,
    UITypes.PYQTCheckButton: QtControllerBase,
    UITypes.PYQTComboBox: QtControllerBase,
    UITypes.PYQTComboBoxNoEdit: QtControllerBase,
    UITypes.PYQTTabControl: QtControllerBase,
    UITypes.PYQTSplitter: QtControllerBase,
    UITypes.PYQTListWidget: QtControllerBase,
    UITypes.PYQTTreeWidget: QtControllerBase,
    UITypes.PYQTTableWidget: QtControllerBase,
    UITypes.PYQTListView: QtControllerBase,
    UITypes.PYQTTreeView: QtControllerBase,
    UITypes.PYQTTableView: QtControllerBase,
    UITypes.PYQTColumnView: QtControllerBase,

    UITypes.PYSIDEWindow: QtControllerBase,
    UITypes.PYSIDELineEdit: QtControllerBase,
    UITypes.PYSIDECheckBox: QtControllerBase,
    UITypes.PYSIDECheckBoxTri: QtControllerBase,
    UITypes.PYSIDERadioButton: QtControllerBase,
    UITypes.PYSIDECheckButton: QtControllerBase,
    UITypes.PYSIDEComboBox: QtControllerBase,
    UITypes.PYSIDEComboBoxNoEdit: QtControllerBase,
    UITypes.PYSIDETabControl: QtControllerBase,
    UITypes.PYSIDESplitter: QtControllerBase,
    UITypes.PYSIDEListWidget: QtControllerBase,
    UITypes.PYSIDETreeWidget: QtControllerBase,
    UITypes.PYSIDETableWidget: QtControllerBase,
    UITypes.PYSIDEListView: QtControllerBase,
    UITypes.PYSIDETreeView: QtControllerBase,
    UITypes.PYSIDETableView: QtControllerBase,
    UITypes.PYSIDEColumnView: QtControllerBase,
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

