import os

import maya.cmds as m

from fxpt.fx_refSystem.com import getMayaQMainWindow, globalPrefsHandler, getRelativePath
from fxpt.fx_refSystem.replace_with_ref_dialog import ReplaceDialog
from fxpt.fx_refSystem.ref_handle import ATTR_REF_SOURCE_PATH
from fxpt.fx_utils.utils import cleanupPath

from fxpt.fx_utils.watch import watch, wtrace

dlg = None

# TODO: need to reload references in scene if they were saved during replace


def replaceRefs():

    nodes = m.ls(sl=True, l=True, typ='transform')
    if not nodes:
        return

    replaceDB = generateReplaceDB(nodes)

    shortcutsExists = any([p for p in replaceDB.values()])
    anonymousExists = any([not p for p in replaceDB.values()])

    shortcutsDuplicatesExists = False
    sDuplicates = set()
    for path in replaceDB.values():
        p = os.path.expandvars(path).lower()
        if p in sDuplicates:
            shortcutsDuplicatesExists = True
            break
        sDuplicates.add(p)

    showDialog(shortcutsExists, shortcutsDuplicatesExists, anonymousExists)

    dlgResult = dlg.getDialogResult()
    if dlgResult == ReplaceDialog.RESULT_CANCEL:
        return

    if anonymousExists:
        sourceFilename = browseForSource()
        if not sourceFilename:
            return
        else:
            for key in replaceDB:
                replaceDB[key] = sourceFilename

    if dlgResult == ReplaceDialog.RESULT_SAVE_REPLACE:
        saveRefsSources(replaceDB)

    doReplacement(replaceDB)


def saveRefsSources(replaceDB):
    pass


def doReplacement(replaceDB):
    pass
    # for tr, path in replaceDB:
    #     refHandle = RefHandle()
    #     refHandle.createNew(refFilename)
    #     return refHandle.refLocator.transform



def showDialog(shortcutsExists, shortcutsDuplicatesExists, anonymousExists):
    if shortcutsExists and not shortcutsDuplicatesExists and not anonymousExists:
        text = "All transforms you've selected contains original reference source paths.<br>" \
               "They will be replaced to their respective sources.<br><br>" \
               "Choose your option."
    elif shortcutsExists and shortcutsDuplicatesExists and not anonymousExists:
        text = "All transforms you've selected contains original reference source paths.<br>" \
               "They will be replaced to their respective sources.<br><br>" \
               "<font color='DarkOrange'><b>WARNING!</b></font> You've got several transforms " \
               "pointing to the same source scene.<br>" \
               "If you choose <b>Save And Replace</b>, one of these transforms will be randomly chosen " \
               "to save as source scene and you may loose your edits.<br><br>" \
               "Choose your option."
    elif shortcutsExists and anonymousExists:
        text = "You've got mixed selection of transforms with and without original reference source paths data.<br><br>" \
               "<font color='DarkOrange'><b>WARNING!</b></font> If you choose <b>Save And Replace</b> or <b>Replace</b>, " \
               "you will be prompted to choose original reference source scene and <font color='white'><b>ALL " \
               "selected transforms will be replaced with the chosen one</b></font>.<br><br>" \
               "Choose your option."
    elif not shortcutsExists and anonymousExists:
        text = "All transforms you've selected does not contain original reference source paths.<br>" \
               "If you choose <b>Save And Replace</b> or <b>Replace</b>, " \
               "you will be prompted to choose original reference source scene and all " \
               "selected transforms will be replaced with the chosen one.<br><br>" \
               "Choose your option."
    else:
        text = "Choose your option."

    global dlg
    if not dlg:
        mayaMainWin = getMayaQMainWindow()
        dlg = ReplaceDialog(mayaMainWin)
    dlg.setText(text)
    dlg.exec_()


def generateReplaceDB(nodes):
    res = {}
    for node in nodes:
        refPathAttr = '{}.{}'.format(node, ATTR_REF_SOURCE_PATH)
        if m.objExists(refPathAttr):
            res[node] = m.getAttr(refPathAttr)
        else:
            res[node] = ''
    return res


def browseForSource():
    globalPrefsHandler.loadPrefs()
    lastBrowsed = globalPrefsHandler.getValue(globalPrefsHandler.KEY_LAST_BROWSED_SOURCE) or ''

    filename = m.fileDialog2(
        dialogStyle=1,
        caption='Choose Reference Scene',
        fileFilter='Maya Scenes (*.mb; *.ma);;Maya Binary (*.mb);;Maya ASCII (*.ma);;All Files (*.*)',
        fileMode=0,
        returnFilter=False,
        startingDirectory=lastBrowsed
    )
    if not filename:
        return None

    filename = cleanupPath(filename[0])

    globalPrefsHandler.setValue(globalPrefsHandler.KEY_LAST_BROWSED_SOURCE, cleanupPath(os.path.dirname(filename)))
    globalPrefsHandler.savePrefs()

    return getRelativePath(filename)
