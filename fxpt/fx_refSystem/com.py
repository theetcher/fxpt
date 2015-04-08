import maya.cmds as m


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
