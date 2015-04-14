import os

import maya.cmds as m

from fxpt.fx_refSystem.com import getMayaQMainWindow, globalPrefsHandler, getRelativePath
from fxpt.fx_refSystem.replace_with_ref_dialog import ReplaceDialog
from fxpt.fx_refSystem.ref_handle import RefHandle, ATTR_REF_SOURCE_PATH
from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_utils.utilsMaya import getParent

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

    logStrings = []

    if dlgResult == ReplaceDialog.RESULT_SAVE_REPLACE:
        logStrings.extend(saveRefsSources(replaceDB))

    log, createdRefs = doReplacement(replaceDB)
    logStrings.extend(log)

    savedSources = []

    return logStrings, createdRefs, savedSources


def saveRefsSources(replaceDB):
    logStrings = []
    return logStrings


def doReplacement(replaceDB):
    notExistingSources = set()
    notExistPathsToLog = set()
    createdRefs = []
    for tr, path in replaceDB.items():

        filename = os.path.expandvars(path).lower()

        if filename in notExistingSources:
            continue

        if not os.path.exists(filename):
            notExistingSources.add(filename)
            notExistPathsToLog.add(path)
            continue

        refHandle = RefHandle()
        refHandle.createNew(path)

        worldRP = m.xform(tr, q=True, rotatePivot=True, worldSpace=True)
        m.move(worldRP[0], worldRP[1], worldRP[2], refHandle.refLocator.transform, absolute=True, worldSpace=True)

        transformParent = getParent(tr)


    logStrings = []
    return logStrings, createdRefs


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
