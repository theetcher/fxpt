_typesCounter = 0


def _getTypeID(typeSet):
    global _typesCounter
    _typesCounter += 1
    return typeSet + _typesCounter


# noinspection PySetFunctionToLiteral
class UIType(object):

    TypesMisc = 0x0100
    TypesPYQT = 0x0200
    TypesPYSIDE = 0x0400
    TypesM = 0x0800
    TypesPM = 0x1000
    TypesAll = TypesMisc | TypesPYQT | TypesPYSIDE | TypesM | TypesPM

    # PyQt Types
    PYQTWindow = _getTypeID(TypesPYQT)
    PYQTLineEdit = _getTypeID(TypesPYQT)
    PYQTCheckBox = _getTypeID(TypesPYQT)
    PYQTCheckAction = _getTypeID(TypesPYQT)
    PYQTSpinBox = _getTypeID(TypesPYQT)
    PYQTDoubleSpinBox = _getTypeID(TypesPYQT)
    PYQTTimeEdit = _getTypeID(TypesPYQT)
    PYQTDateEdit = _getTypeID(TypesPYQT)
    PYQTDateTimeEdit = _getTypeID(TypesPYQT)
    PYQTRadioButton = _getTypeID(TypesPYQT)
    PYQTCheckButton = _getTypeID(TypesPYQT)
    PYQTComboBox = _getTypeID(TypesPYQT)
    PYQTComboBoxEditable = _getTypeID(TypesPYQT)
    PYQTTabWidget = _getTypeID(TypesPYQT)
    PYQTStackedWidget = _getTypeID(TypesPYQT)
    PYQTToolBox = _getTypeID(TypesPYQT)
    PYQTSplitter = _getTypeID(TypesPYQT)
    PYQTScrollBar = _getTypeID(TypesPYQT)
    PYQTScrollArea = _getTypeID(TypesPYQT)
    PYQTSlider = _getTypeID(TypesPYQT)
    PYQTDial = _getTypeID(TypesPYQT)
    PYQTTextEdit = _getTypeID(TypesPYQT)
    PYQTPlainTextEdit = _getTypeID(TypesPYQT)
    PYQTListWidget = _getTypeID(TypesPYQT)
    PYQTTreeWidget = _getTypeID(TypesPYQT)
    PYQTTableWidget = _getTypeID(TypesPYQT)
    PYQTListView = _getTypeID(TypesPYQT)
    PYQTTreeView = _getTypeID(TypesPYQT)
    PYQTTableView = _getTypeID(TypesPYQT)

    # PySide Types
    PYSIDEWindow = _getTypeID(TypesPYSIDE)
    PYSIDELineEdit = _getTypeID(TypesPYSIDE)
    PYSIDECheckBox = _getTypeID(TypesPYSIDE)
    PYSIDECheckAction = _getTypeID(TypesPYQT)
    PYSIDESpinBox = _getTypeID(TypesPYSIDE)
    PYSIDEDoubleSpinBox = _getTypeID(TypesPYSIDE)
    PYSIDETimeEdit = _getTypeID(TypesPYSIDE)
    PYSIDEDateEdit = _getTypeID(TypesPYSIDE)
    PYSIDEDateTimeEdit = _getTypeID(TypesPYSIDE)
    PYSIDERadioButton = _getTypeID(TypesPYSIDE)
    PYSIDECheckButton = _getTypeID(TypesPYSIDE)
    PYSIDEComboBox = _getTypeID(TypesPYSIDE)
    PYSIDEComboBoxEditable = _getTypeID(TypesPYSIDE)
    PYSIDETabWidget = _getTypeID(TypesPYSIDE)
    PYSIDEStackedWidget = _getTypeID(TypesPYSIDE)
    PYSIDEToolBox = _getTypeID(TypesPYSIDE)
    PYSIDESplitter = _getTypeID(TypesPYSIDE)
    PYSIDEScrollBar = _getTypeID(TypesPYSIDE)
    PYSIDEScrollArea = _getTypeID(TypesPYSIDE)
    PYSIDESlider = _getTypeID(TypesPYSIDE)
    PYSIDEDial = _getTypeID(TypesPYSIDE)
    PYSIDETextEdit = _getTypeID(TypesPYSIDE)
    PYSIDEPlainTextEdit = _getTypeID(TypesPYSIDE)
    PYSIDEListWidget = _getTypeID(TypesPYSIDE)
    PYSIDETreeWidget = _getTypeID(TypesPYSIDE)
    PYSIDETableWidget = _getTypeID(TypesPYSIDE)
    PYSIDEListView = _getTypeID(TypesPYSIDE)
    PYSIDETreeView = _getTypeID(TypesPYSIDE)
    PYSIDETableView = _getTypeID(TypesPYSIDE)

    # Maya Types
    MCheckBox = _getTypeID(TypesM)
    MCheckBoxGrp1 = _getTypeID(TypesM)
    MCheckBoxGrp2 = _getTypeID(TypesM)
    MCheckBoxGrp3 = _getTypeID(TypesM)
    MCheckBoxGrp4 = _getTypeID(TypesM)
    MColorSliderGrp = _getTypeID(TypesM)
    MFloatField = _getTypeID(TypesM)
    MFloatFieldGrp1 = _getTypeID(TypesM)
    MFloatFieldGrp2 = _getTypeID(TypesM)
    MFloatFieldGrp3 = _getTypeID(TypesM)
    MFloatFieldGrp4 = _getTypeID(TypesM)
    MFloatScrollBar = _getTypeID(TypesM)
    MFloatSlider = _getTypeID(TypesM)
    MFloatSliderGrp = _getTypeID(TypesM)
    MFrameLayout = _getTypeID(TypesM)
    MIconTextCheckBox = _getTypeID(TypesM)
    MIconTextRadioButton = _getTypeID(TypesM)
    MIconTextScrollList = _getTypeID(TypesM)
    MIntField = _getTypeID(TypesM)
    MIntFieldGrp1 = _getTypeID(TypesM)
    MIntFieldGrp2 = _getTypeID(TypesM)
    MIntFieldGrp3 = _getTypeID(TypesM)
    MIntFieldGrp4 = _getTypeID(TypesM)
    MIntScrollBar = _getTypeID(TypesM)
    MIntSlider = _getTypeID(TypesM)
    MIntSliderGrp = _getTypeID(TypesM)
    MOptionMenu = _getTypeID(TypesM)
    MOptionMenuGrp = _getTypeID(TypesM)
    MRadioButton = _getTypeID(TypesM)
    MRadioButtonGrp1 = _getTypeID(TypesM)
    MRadioButtonGrp2 = _getTypeID(TypesM)
    MRadioButtonGrp3 = _getTypeID(TypesM)
    MRadioButtonGrp4 = _getTypeID(TypesM)
    MSymbolCheckBox = _getTypeID(TypesM)
    MScriptTable = _getTypeID(TypesM)
    MScrollField = _getTypeID(TypesM)
    MScrollLayout = _getTypeID(TypesM)
    MShelfTabLayout = _getTypeID(TypesM)
    MTabLayout = _getTypeID(TypesM)
    MTextField = _getTypeID(TypesM)
    MTextFieldButtonGrp = _getTypeID(TypesM)
    MTextFieldGrp = _getTypeID(TypesM)
    MTextScrollList = _getTypeID(TypesM)

    # PyMel Types
    PMCheckBox = _getTypeID(TypesPM)
    PMCheckBoxGrp1 = _getTypeID(TypesPM)
    PMCheckBoxGrp2 = _getTypeID(TypesPM)
    PMCheckBoxGrp3 = _getTypeID(TypesPM)
    PMCheckBoxGrp4 = _getTypeID(TypesPM)
    PMColorSliderGrp = _getTypeID(TypesPM)
    PMFloatField = _getTypeID(TypesPM)
    PMFloatFieldGrp1 = _getTypeID(TypesPM)
    PMFloatFieldGrp2 = _getTypeID(TypesPM)
    PMFloatFieldGrp3 = _getTypeID(TypesPM)
    PMFloatFieldGrp4 = _getTypeID(TypesPM)
    PMFloatScrollBar = _getTypeID(TypesPM)
    PMFloatSlider = _getTypeID(TypesPM)
    PMFloatSliderGrp = _getTypeID(TypesPM)
    PMFrameLayout = _getTypeID(TypesPM)
    PMIconTextCheckBox = _getTypeID(TypesPM)
    PMIconTextRadioButton = _getTypeID(TypesPM)
    PMIconTextScrollList = _getTypeID(TypesPM)
    PMIntField = _getTypeID(TypesPM)
    PMIntFieldGrp1 = _getTypeID(TypesPM)
    PMIntFieldGrp2 = _getTypeID(TypesPM)
    PMIntFieldGrp3 = _getTypeID(TypesPM)
    PMIntFieldGrp4 = _getTypeID(TypesPM)
    PMIntScrollBar = _getTypeID(TypesPM)
    PMIntSlider = _getTypeID(TypesPM)
    PMIntSliderGrp = _getTypeID(TypesPM)
    PMOptionMenu = _getTypeID(TypesPM)
    PMOptionMenuGrp = _getTypeID(TypesPM)
    PMRadioButton = _getTypeID(TypesPM)
    PMRadioButtonGrp1 = _getTypeID(TypesPM)
    PMRadioButtonGrp2 = _getTypeID(TypesPM)
    PMRadioButtonGrp3 = _getTypeID(TypesPM)
    PMRadioButtonGrp4 = _getTypeID(TypesPM)
    PMSymbolCheckBox = _getTypeID(TypesPM)
    PMScriptTable = _getTypeID(TypesPM)
    PMScrollField = _getTypeID(TypesPM)
    PMScrollLayout = _getTypeID(TypesPM)
    PMShelfTabLayout = _getTypeID(TypesPM)
    PMTabLayout = _getTypeID(TypesPM)
    PMTextField = _getTypeID(TypesPM)
    PMTextFieldButtonGrp = _getTypeID(TypesPM)
    PMTextFieldGrp = _getTypeID(TypesPM)
    PMTextScrollList = _getTypeID(TypesPM)

    @classmethod
    def isTypeOf(cls, t, typeSet):
        return t & typeSet


class Attr(object):

    CheckState = 'checkState'
    Collapsed = 'collapsed'
    CurrentIndex = 'currentIndex'
    ExpandedIndexes = 'expandedIndexes'
    Item = 'item'
    Items = 'items'
    ItemsCount = 'itemCount'
    ScrollValues = 'scrollValues'
    SelectedIndexes = 'selectedIndexes'
    SelectedRanges = 'selectedRanges'
    Sizes = 'sizes'
    SortedSection = 'sortedSection'
    SortingOrder = 'sortingOrder'
    Text = 'text'
    Value = 'value'
    WinGeom = 'winGeom'
