from fxpt.qt.pyside import QtWidgets, isPySide2

from fxpt.fx_prefsaver import prefsaver, serializers

if isPySide2():
    from fxpt.fx_texture_manager.log_dialog_ui2 import Ui_Dialog
else:
    from fxpt.fx_texture_manager.log_dialog_ui import Ui_Dialog

OPT_VAR_NAME_LOG_DLG = 'fx_textureManager_logDlg_prefs'


class LogDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(LogDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME_LOG_DLG))
        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (200, 200, 800, 500))

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def showLog(self, strings):
        if strings:
            self.ui.uiTXT_log.clear()
            for s in strings:
                self.ui.uiTXT_log.appendPlainText(s)
            self.exec_()

    def onDialogFinished(self):
        self.ui_saveSettings()
