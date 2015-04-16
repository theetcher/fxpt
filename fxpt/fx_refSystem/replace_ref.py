import os

import maya.cmds as m

from fxpt.fx_refSystem.com import getMayaQMainWindow, globalPrefsHandler, getRelativePath, expandPath
from fxpt.fx_refSystem.log_dialog import log
from fxpt.fx_refSystem.replace_with_ref_dialog import ReplaceDialog
from fxpt.fx_refSystem.ref_handle import RefHandle, ATTR_REF_SOURCE_PATH
from fxpt.fx_refSystem.transform_handle import TransformHandle
from fxpt.fx_utils.utils import cleanupPath, makeWritable
from fxpt.fx_utils.utilsMaya import getParent, getShape, getChildTransforms, getLongName, getShortName

from fxpt.fx_utils.watch import watch, wtrace

dlg = None

# TODO: need to reload references in scene if they were saved during replace


def replaceRefs():

    nodes = m.ls(sl=True, l=True, typ='transform')
    if not nodes:
        return None, None

    if isBadSelection(nodes):
        log.logAppend("Invalid selection: you've selected both a parent and a child. Reference replacement aborted.")
        return None, None

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
        return None, None

    if anonymousExists:
        sourceFilename = browseForSource(0 if dlgResult == ReplaceDialog.RESULT_SAVE_REPLACE else 1)
        if not sourceFilename:
            return None, None
        else:
            for key in replaceDB:
                replaceDB[key] = sourceFilename

    savedSources = []
    if dlgResult == ReplaceDialog.RESULT_SAVE_REPLACE:
        savedSources = saveRefsSources(replaceDB)

    createdRefs = doReplacement(replaceDB)

    return createdRefs, savedSources


def saveRefsSources(replaceDB):

    processedPaths = set()
    for tr, path in replaceDB.items():
        if not m.objExists(tr):
            continue

        expandedPath = expandPath(path)
        if expandedPath in processedPaths:
            continue

        shape = getShape(tr)
        childTransforms = getChildTransforms(tr)

        if not shape and not childTransforms:
            log.logAppend('Cannot save empty transform: {}. Source save skipped.'.format(tr))
            continue
        else:
            # cannot save local matrix and restore it cause it resets pivots positions
            translationOrig = m.xform(tr, q=True, translation=True, objectSpace=True)
            rotationOrig = m.xform(tr, q=True, rotation=True, objectSpace=True)
            scaleOrig = m.xform(tr, q=True, scale=True, objectSpace=True, relative=True)
            shearOrig = m.xform(tr, q=True, shear=True, objectSpace=True, relative=True)
            shortNameOrig = getShortName(tr)

            oldParent = getParent(tr)
            if oldParent:
                newObject = m.parent(tr, world=True)[0]
            else:
                newObject = tr

            worldRP = m.xform(newObject, q=True, rotatePivot=True, worldSpace=True)
            m.xform(newObject, relative=True, worldSpace=True, translation=[-x for x in worldRP])
            m.xform(newObject, absolute=True, rotation=(0, 0, 0), scale=(1, 1, 1), shear=(0, 0, 0))

            if shape:
                m.select(newObject, r=True)
            else:
                children = getChildTransforms(newObject)
                if children:
                    newChildren = m.parent(children, world=True)
                m.select(newChildren, r=True)

            ext = os.path.splitext(path)[1]
            watch(path, 'saving path')
            makeWritable(expandPath(path))
            m.file(
                path,
                exportSelected=True,
                force=True,
                typ='mayaBinary' if ext == '.mb' else 'mayaAscii',
                options='v=0;'
            )

            if not shape:
                m.delete(newChildren)

            if oldParent:
                newObject2 = m.parent(newObject, oldParent)[0]
            else:
                newObject2 = newObject

            m.xform(newObject2, objectSpace=True, absolute=True, translation=translationOrig, rotation=rotationOrig, scale=scaleOrig, shear=shearOrig)

            if getShortName(newObject2) != shortNameOrig:
                m.rename(newObject2, shortNameOrig)

        processedPaths.add(expandedPath)

    return processedPaths


def doReplacement(replaceDB):
    notExistingSources = set()
    createdRefs = []
    for tr, path in replaceDB.items():

        if path in notExistingSources:
            continue

        if not os.path.exists(os.path.expandvars(path)):
            notExistingSources.add(path)
            log.logAppend('Path does not exists: {}. Replacement skipped.'.format(path))
            continue

        refHandle = RefHandle()
        refHandle.createNew(path)
        createdRefs.append(refHandle)

        worldRP = m.xform(tr, q=True, rotatePivot=True, worldSpace=True)
        m.xform(refHandle.refLocator.transform, translation=worldRP, absolute=True, worldSpace=True)

        transformParent = getParent(tr)
        if transformParent:
            newRefLocTransform = getLongName(m.parent(refHandle.refLocator.transform, transformParent)[0])
            refHandle.setRefLocator(TransformHandle(transform=newRefLocTransform))

        rotation = m.xform(tr, q=True, rotation=True, objectSpace=True)
        scale = m.xform(tr, q=True, scale=True, objectSpace=True, relative=True)
        shear = m.xform(tr, q=True, shear=True, objectSpace=True, relative=True)
        m.xform(refHandle.refLocator.transform, rotation=rotation, scale=scale, shear=shear)

        if m.objExists(tr):
            m.delete(tr)

    return createdRefs


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
               "<font color='DarkOrange'><b>WARNING!</b></font> " \
               "You will be prompted to choose or save original reference source scene.<br>" \
               "In case of <b>Save And Replace</b>, a random selected transform will be chosen to save as source scene.<br>" \
               "In both <b>Save And Replace</b> and <b>Replace</b> cases <font color='white'><b>ALL " \
               "selected transforms will be replaced with the chosen one</b></font><br><br>" \
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


def browseForSource(fileMode):
    globalPrefsHandler.loadPrefs()
    lastBrowsed = globalPrefsHandler.getValue(globalPrefsHandler.KEY_LAST_BROWSED_SOURCE) or ''

    filename = m.fileDialog2(
        dialogStyle=1,
        caption='Choose Reference Scene',
        fileFilter='Maya Scenes (*.mb; *.ma);;Maya Binary (*.mb);;Maya ASCII (*.ma);;All Files (*.*)',
        fileMode=fileMode,
        returnFilter=False,
        startingDirectory=lastBrowsed
    )
    if not filename:
        return None

    filename = cleanupPath(filename[0])

    globalPrefsHandler.setValue(globalPrefsHandler.KEY_LAST_BROWSED_SOURCE, cleanupPath(os.path.dirname(filename)))
    globalPrefsHandler.savePrefs()

    return getRelativePath(filename)


def isBadSelection(nodes):
    nodes = [n + '|' for n in sorted(nodes)]
    lenNodes = len(nodes)
    for i in range(lenNodes):
        for j in range(i + 1, lenNodes):
            if nodes[j].startswith(nodes[i]):
                return True
    return False