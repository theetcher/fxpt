import maya.cmds as m

from global_prefs_handler import GlobalPrefsHandler

globalPrefsHandler = GlobalPrefsHandler()

REF_ROOT_VAR_NAME = 'FX_REF_ROOT'
REF_ROOT_VAR_NAME_P = '%{}%'.format(REF_ROOT_VAR_NAME)


def messageBoxMaya(message, title='Error', icon='critical', button=['Close'], defaultButton='Close', cancelButton='Close', dismissString='Close'):
    return m.confirmDialog(
        title=title,
        message=message,
        button=button,
        defaultButton=defaultButton,
        cancelButton=cancelButton,
        dismissString=dismissString,
        icon=icon
    )
