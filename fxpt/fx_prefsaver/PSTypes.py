# noinspection PySetFunctionToLiteral
class UIType(object):

    # PyQt Types
    PYQTWindow = 1
    PYQTLineEdit = 2
    PYQTCheckBox = 3
    PYQTSpinBox = 4
    PYQTDoubleSpinBox = 5
    PYQTTimeEdit = 6
    PYQTDateEdit = 7
    PYQTDateTimeEdit = 8
    PYQTRadioButton = 9
    PYQTCheckButton = 10
    PYQTComboBox = 11
    PYQTComboBoxEditable = 12
    PYQTTabWidget = 13
    PYQTStackedWidget = 14
    PYQTToolBox = 15
    PYQTSplitter = 16
    PYQTScrollBar = 17
    PYQTScrollArea = 18
    PYQTSlider = 19
    PYQTDial = 20
    PYQTTextEdit = 21
    PYQTPlainTextEdit = 22
    PYQTListWidget = 23
    PYQTTreeWidget = 24
    PYQTTableWidget = 25
    PYQTListView = 26
    PYQTTreeView = 27
    PYQTTableView = 28

    TypesPYQT = set([
        PYQTWindow,
        PYQTLineEdit,
        PYQTCheckBox,
        PYQTSpinBox,
        PYQTDoubleSpinBox,
        PYQTTimeEdit,
        PYQTDateEdit,
        PYQTDateTimeEdit,
        PYQTRadioButton,
        PYQTCheckButton,
        PYQTComboBox,
        PYQTComboBoxEditable,
        PYQTTabWidget,
        PYQTStackedWidget,
        PYQTToolBox,
        PYQTSplitter,
        PYQTScrollBar,
        PYQTScrollArea,
        PYQTSlider,
        PYQTDial,
        PYQTTextEdit,
        PYQTPlainTextEdit,
        PYQTListWidget,
        PYQTTreeWidget,
        PYQTTableWidget,
        PYQTListView,
        PYQTTreeView,
        PYQTTableView
    ])

    # TypesPYSIDE_Flag = 0x010000
    # TypesPYSIDE_Flag = 0x020000
    # TypesPYSIDE_Flag = 0x040000

    # PySide Types
    # PYSIDEWindow = next(TypesPYSIDE_Flag)
    # PYSIDELineEdit = TypesPYSIDE_Flag + 102
    PYSIDEWindow = 101
    PYSIDELineEdit = 102
    PYSIDECheckBox = 103
    PYSIDESpinBox = 104
    PYSIDEDoubleSpinBox = 105
    PYSIDETimeEdit = 106
    PYSIDEDateEdit = 107
    PYSIDEDateTimeEdit = 108
    PYSIDERadioButton = 109
    PYSIDECheckButton = 110
    PYSIDEComboBox = 111
    PYSIDEComboBoxEditable = 112
    PYSIDETabWidget = 113
    PYSIDEStackedWidget = 114
    PYSIDEToolBox = 115
    PYSIDESplitter = 116
    PYSIDEScrollBar = 117
    PYSIDEScrollArea = 118
    PYSIDESlider = 119
    PYSIDEDial = 120
    PYSIDETextEdit = 121
    PYSIDEPlainTextEdit = 122
    PYSIDEListWidget = 123
    PYSIDETreeWidget = 124
    PYSIDETableWidget = 125
    PYSIDEListView = 126
    PYSIDETreeView = 127
    PYSIDETableView = 128

    TypesPYSIDE = set([
        PYSIDEWindow,
        PYSIDELineEdit,
        PYSIDECheckBox,
        PYSIDESpinBox,
        PYSIDEDoubleSpinBox,
        PYSIDETimeEdit,
        PYSIDEDateEdit,
        PYSIDEDateTimeEdit,
        PYSIDERadioButton,
        PYSIDECheckButton,
        PYSIDEComboBox,
        PYSIDEComboBoxEditable,
        PYSIDETabWidget,
        PYSIDEStackedWidget,
        PYSIDEToolBox,
        PYSIDESplitter,
        PYSIDEScrollBar,
        PYSIDEScrollArea,
        PYSIDESlider,
        PYSIDEDial,
        PYSIDETextEdit,
        PYSIDEPlainTextEdit,
        PYSIDEListWidget,
        PYSIDETreeWidget,
        PYSIDETableWidget,
        PYSIDEListView,
        PYSIDETreeView,
        PYSIDETableView
    ])

    # Maya Types
    MCheckBox = 201
    MCheckBoxGrp1 = 202
    MCheckBoxGrp2 = 203
    MCheckBoxGrp3 = 204
    MCheckBoxGrp4 = 205
    MColorSliderGrp = 206
    MFloatField = 207
    MFloatFieldGrp1 = 208
    MFloatFieldGrp2 = 209
    MFloatFieldGrp3 = 210
    MFloatFieldGrp4 = 211
    MFloatScrollBar = 212
    MFloatSlider = 213
    MFloatSliderGrp = 215
    MFrameLayout = 216
    MIconTextCheckBox = 217
    MIconTextRadioButton = 218
    MIconTextScrollList = 219
    MIntField = 220
    MIntFieldGrp1 = 221
    MIntFieldGrp2 = 222
    MIntFieldGrp3 = 223
    MIntFieldGrp4 = 224
    MIntScrollBar = 225
    MIntSlider = 226
    MIntSliderGrp = 227
    MOptionMenu = 228
    MOptionMenuGrp = 229
    MRadioButton = 230
    MRadioButtonGrp1 = 231
    MRadioButtonGrp2 = 232
    MRadioButtonGrp3 = 233
    MRadioButtonGrp4 = 234
    MSymbolCheckBox = 235
    MScriptTable = 236
    MScrollField = 237
    MScrollLayout = 238
    MShelfTabLayout = 239
    MTabLayout = 240
    MTextField = 241
    MTextFieldButtonGrp = 242
    MTextFieldGrp = 243
    MTextScrollList = 244

    TypesM = set([
        MCheckBox,
        MCheckBoxGrp1,
        MCheckBoxGrp2,
        MCheckBoxGrp3,
        MCheckBoxGrp4,
        MColorSliderGrp,
        MFloatField,
        MFloatFieldGrp1,
        MFloatFieldGrp2,
        MFloatFieldGrp3,
        MFloatFieldGrp4,
        MFloatScrollBar,
        MFloatSlider,
        MFloatSliderGrp,
        MFrameLayout,
        MIconTextCheckBox,
        MIconTextRadioButton,
        MIconTextScrollList,
        MIntField,
        MIntFieldGrp1,
        MIntFieldGrp2,
        MIntFieldGrp3,
        MIntFieldGrp4,
        MIntScrollBar,
        MIntSlider,
        MIntSliderGrp,
        MOptionMenu,
        MOptionMenuGrp,
        MRadioButton,
        MRadioButtonGrp1,
        MRadioButtonGrp2,
        MRadioButtonGrp3,
        MRadioButtonGrp4,
        MSymbolCheckBox,
        MScriptTable,
        MScrollField,
        MScrollLayout,
        MShelfTabLayout,
        MTabLayout,
        MTextField,
        MTextFieldButtonGrp,
        MTextFieldGrp,
        MTextScrollList,
    ])

    # PyMel Types
    PMCheckBox = 301
    PMCheckBoxGrp1 = 302
    PMCheckBoxGrp2 = 303
    PMCheckBoxGrp3 = 304
    PMCheckBoxGrp4 = 305
    PMColorSliderGrp = 306
    PMFloatField = 307
    PMFloatFieldGrp1 = 308
    PMFloatFieldGrp2 = 309
    PMFloatFieldGrp3 = 310
    PMFloatFieldGrp4 = 311
    PMFloatScrollBar = 312
    PMFloatSlider = 313
    PMFloatSliderGrp = 315
    PMFrameLayout = 316
    PMIconTextCheckBox = 317
    PMIconTextRadioButton = 318
    PMIconTextScrollList = 319
    PMIntField = 320
    PMIntFieldGrp1 = 321
    PMIntFieldGrp2 = 322
    PMIntFieldGrp3 = 323
    PMIntFieldGrp4 = 324
    PMIntScrollBar = 325
    PMIntSlider = 326
    PMIntSliderGrp = 327
    PMOptionMenu = 328
    PMOptionMenuGrp = 329
    PMRadioButton = 330
    PMRadioButtonGrp1 = 331
    PMRadioButtonGrp2 = 332
    PMRadioButtonGrp3 = 333
    PMRadioButtonGrp4 = 334
    PMSymbolCheckBox = 335
    PMScriptTable = 336
    PMScrollField = 337
    PMScrollLayout = 338
    PMShelfTabLayout = 339
    PMTabLayout = 340
    PMTextField = 341
    PMTextFieldButtonGrp = 342
    PMTextFieldGrp = 343
    PMTextScrollList = 344

    TypesPM = set([
        PMCheckBox,
        PMCheckBoxGrp1,
        PMCheckBoxGrp2,
        PMCheckBoxGrp3,
        PMCheckBoxGrp4,
        PMColorSliderGrp,
        PMFloatField,
        PMFloatFieldGrp1,
        PMFloatFieldGrp2,
        PMFloatFieldGrp3,
        PMFloatFieldGrp4,
        PMFloatScrollBar,
        PMFloatSlider,
        PMFloatSliderGrp,
        PMFrameLayout,
        PMIconTextCheckBox,
        PMIconTextRadioButton,
        PMIconTextScrollList,
        PMIntField,
        PMIntFieldGrp1,
        PMIntFieldGrp2,
        PMIntFieldGrp3,
        PMIntFieldGrp4,
        PMIntScrollBar,
        PMIntSlider,
        PMIntSliderGrp,
        PMOptionMenu,
        PMOptionMenuGrp,
        PMRadioButton,
        PMRadioButtonGrp1,
        PMRadioButtonGrp2,
        PMRadioButtonGrp3,
        PMRadioButtonGrp4,
        PMSymbolCheckBox,
        PMScriptTable,
        PMScrollField,
        PMScrollLayout,
        PMShelfTabLayout,
        PMTabLayout,
        PMTextField,
        PMTextFieldButtonGrp,
        PMTextFieldGrp,
        PMTextScrollList
    ])

    # Misc
    Variable = 401
    VariableOptVar = 402

    TypesAll = TypesPYQT | TypesPYSIDE | TypesM | TypesPM


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
