from fxpt.qt.pyside import QtWidgets, isPySide2

from fxpt.fx_prefsaver import prefsaver, serializers

if isPySide2():
    from fxpt.fx_texture_manager.search_replace_dialog_ui2 import Ui_Dialog
else:
    from fxpt.fx_texture_manager.search_replace_dialog_ui import Ui_Dialog

OPT_VAR_NAME_SEARCH_REPLACE_DLG = 'fx_textureManager_searchReplaceDlg_prefs'


class SearchReplaceDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(SearchReplaceDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME_SEARCH_REPLACE_DLG))

        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (200, 200, 600, 100))
        self.prefSaver.addControl(self.ui.uiLED_search, prefsaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiLED_replace, prefsaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiCHK_caseSensitive, prefsaver.UIType.PYSIDECheckBox, False)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def getDialogData(self):
        return str(self.ui.uiLED_search.text()), str(self.ui.uiLED_replace.text()), self.ui.uiCHK_caseSensitive.isChecked()

    def onDialogAccepted(self):
        self.ui_saveSettings()
