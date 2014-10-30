# noinspection PySetFunctionToLiteral
class UITypes(object):

    # PyQt Types
    PYQTWindow = 1
    PYQTLineEdit = 2
    PYQTCheckBox = 3
    PYQTCheckBoxTri = 4
    PYQTRadioButton = 5
    PYQTCheckButton = 6
    PYQTComboBox = 7
    PYQTComboBoxNoEdit = 8
    PYQTTabControl = 9
    PYQTSplitter = 10
    PYQTListWidget = 11
    PYQTTreeWidget = 12
    PYQTTableWidget = 13
    PYQTListView = 14
    PYQTTreeView = 15
    PYQTTableView = 16
    PYQTColumnView = 17

    TypesPYQT = set([
        PYQTWindow,
        PYQTLineEdit,
        PYQTCheckBox,
        PYQTCheckBoxTri,
        PYQTRadioButton,
        PYQTCheckButton,
        PYQTComboBox,
        PYQTComboBoxNoEdit,
        PYQTTabControl,
        PYQTSplitter,
        PYQTListWidget,
        PYQTTreeWidget,
        PYQTTableWidget,
        PYQTListView,
        PYQTTreeView,
        PYQTTableView,
        PYQTColumnView
    ])

    # PySide Types
    PYSIDEWindow = 101
    PYSIDELineEdit = 102
    PYSIDECheckBox = 103
    PYSIDECheckBoxTri = 104
    PYSIDERadioButton = 105
    PYSIDECheckButton = 106
    PYSIDEComboBox = 107
    PYSIDEComboBoxNoEdit = 108
    PYSIDETabControl = 109
    PYSIDESplitter = 110
    PYSIDEListWidget = 111
    PYSIDETreeWidget = 112
    PYSIDETableWidget = 113
    PYSIDEListView = 114
    PYSIDETreeView = 115
    PYSIDETableView = 116
    PYSIDEColumnView = 117

    TypesPYSIDE = set([
        PYSIDEWindow,
        PYSIDELineEdit,
        PYSIDECheckBox,
        PYSIDECheckBoxTri,
        PYSIDERadioButton,
        PYSIDECheckButton,
        PYSIDEComboBox,
        PYSIDEComboBoxNoEdit,
        PYSIDETabControl,
        PYSIDESplitter,
        PYSIDEListWidget,
        PYSIDETreeWidget,
        PYSIDETableWidget,
        PYSIDEListView,
        PYSIDETreeView,
        PYSIDETableView,
        PYSIDEColumnView
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
    MFloatSliderGrp = 214
    MFrameLayout = 215
    MIconTextCheckBox = 216
    MIconTextRadioButton = 217
    MIconTextScrollList = 218  # same as MTextScrollList
    MIntField = 219
    MIntFieldGrp1 = 220
    MIntFieldGrp2 = 221
    MIntFieldGrp3 = 222
    MIntFieldGrp4 = 223
    MIntScrollBar = 224
    MIntSlider = 225
    MIntSliderGrp = 226
    MRadioButton = 227
    MRadioButtonGrp1 = 228
    MRadioButtonGrp2 = 229
    MRadioButtonGrp3 = 230
    MRadioButtonGrp4 = 231
    MSymbolCheckBox = 232
    MScriptTable = 233
    MScrollField = 234  # the same as MTextField
    MScrollLayout = 235
    MShelfTabLayout = 236
    MSwitchTable = 237
    MTabLayout = 238
    MTextField = 239
    MTextFieldButtonGrp = 240
    MTextFieldGrp = 241
    MTextScrollList = 242

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
        MIconTextScrollList,  # same as MTextScrollList
        MIntField,
        MIntFieldGrp1,
        MIntFieldGrp2,
        MIntFieldGrp3,
        MIntFieldGrp4,
        MIntScrollBar,
        MIntSlider,
        MIntSliderGrp,
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
        MSwitchTable,
        MTabLayout,
        MTextField,
        MTextFieldButtonGrp,
        MTextFieldGrp,
        MTextScrollList
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
    PMFloatSlider2 = 314
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
    PMRadioButton = 328
    PMRadioButtonGrp1 = 329
    PMRadioButtonGrp2 = 330
    PMRadioButtonGrp3 = 331
    PMRadioButtonGrp4 = 332
    PMSymbolCheckBox = 333
    PMScriptTable = 334
    PMScrollField = 335  # the same as PMTextField
    PMScrollLayout = 336
    PMShelfTabLayout = 337
    PMTabLayout = 338
    PMTextField = 339
    PMTextFieldButtonGrp = 340
    PMTextFieldGrp = 341
    PMTextScrollList = 342

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
        PMFloatSlider2,
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

    # Constructors = {
    #     QtWindow: QtDescWindow,
    #     QtLineEdit: QtDescLineEdit,
    #     QtCheckBox: QtDescCheckBox,
    #     QtRadioButton: QtDescRadioButton,
    #     QtButton: QtDescButton,
    #     QtComboBox: QtDescComboBox,
    #     QtComboBoxNoEdit: QtDescComboBoxNoEdit,
    #     QtTabControl: QtDescTabControl,
    #     QtSplitter: QtDescSplitter,
    #     QtTableWidget: QtDescTableWidget,
    #     Variable: VarDesc,
    #     VariableOptVar: VarDescOptVar
    # }

