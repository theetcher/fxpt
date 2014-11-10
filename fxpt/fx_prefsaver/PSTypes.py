# noinspection PySetFunctionToLiteral
class UIType(object):

    # PyQt Types
    PYQTWindow = 1
    PYQTLineEdit = 2
    PYQTCheckBox = 3
    PYQTRadioButton = 4
    PYQTCheckButton = 5
    PYQTComboBox = 6
    PYQTComboBoxEditable = 7
    PYQTTabControl = 8
    PYQTSplitter = 9
    PYQTListWidget = 10
    PYQTTreeWidget = 11
    PYQTTableWidget = 12
    PYQTListView = 13
    PYQTTreeView = 14
    PYQTTableView = 15

    TypesPYQT = set([
        PYQTWindow,
        PYQTLineEdit,
        PYQTCheckBox,
        PYQTRadioButton,
        PYQTCheckButton,
        PYQTComboBox,
        PYQTComboBoxEditable,
        PYQTTabControl,
        PYQTSplitter,
        PYQTListWidget,
        PYQTTreeWidget,
        PYQTTableWidget,
        PYQTListView,
        PYQTTreeView,
        PYQTTableView,
    ])

    # PySide Types
    PYSIDEWindow = 101
    PYSIDELineEdit = 102
    PYSIDECheckBox = 103
    PYSIDERadioButton = 104
    PYSIDECheckButton = 105
    PYSIDEComboBox = 106
    PYSIDEComboBoxEditable = 107
    PYSIDETabControl = 108
    PYSIDESplitter = 109
    PYSIDEListWidget = 110
    PYSIDETreeWidget = 111
    PYSIDETableWidget = 112
    PYSIDEListView = 113
    PYSIDETreeView = 114
    PYSIDETableView = 115

    TypesPYSIDE = set([
        PYSIDEWindow,
        PYSIDELineEdit,
        PYSIDECheckBox,
        PYSIDERadioButton,
        PYSIDECheckButton,
        PYSIDEComboBox,
        PYSIDEComboBoxEditable,
        PYSIDETabControl,
        PYSIDESplitter,
        PYSIDEListWidget,
        PYSIDETreeWidget,
        PYSIDETableWidget,
        PYSIDEListView,
        PYSIDETreeView,
        PYSIDETableView,
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
    MFloatSlider2 = 214
    MFloatSliderGrp = 215
    MFrameLayout = 216
    MIconTextCheckBox = 217
    MIconTextRadioButton = 218
    MIconTextScrollList = 219  # same as MTextScrollList
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
    MScrollField = 237  # the same as MTextField
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
        MFloatSlider2,
        MFloatSliderGrp,
        MFrameLayout,
        MIconTextCheckBox,
        MIconTextRadioButton,
        MIconTextScrollList,  # same as MTextScrollList
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
        MScrollField,  # the same as MTextField
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
    # PMFloatSlider2 = 314  # is not implemented cause getFullPathName() stops with an error
    PMFloatSliderGrp = 315
    PMFrameLayout = 316
    PMIconTextCheckBox = 317
    PMIconTextRadioButton = 318
    PMIconTextScrollList = 319  # same as PMTextScrollList
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
    PMScrollField = 337  # the same as PMTextField
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
        # PMFloatSlider2,  # is not implemented cause getFullPathName() stops with an error
        PMFloatSliderGrp,
        PMFrameLayout,
        PMIconTextCheckBox,
        PMIconTextRadioButton,
        PMIconTextScrollList,  # same as PMTextScrollList
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
        PMScrollField,  # the same as PMTextField
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
    ColorRGB = 'colorRGB'
    CurrentIndex = 'currentIndex'
    ExpandedIndexes = 'expandedIndexes'
    Item = 'item'
    ItemsCount = 'itemCount'
    SelectedIndexes = 'selectedIndexes'
    SelectedRanges = 'selectedRanges'
    Sizes = 'sizes'
    SortedSection = 'sortedSection'
    SortingOrder = 'sortingOrder'
    Text = 'text'
    Value = 'value'
    WinGeom = 'winGeom'
