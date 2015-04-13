import os
import re
import math

import maya.cmds as m

from fxpt.fx_refSystem.com import messageBoxMaya, globalPrefsHandler, getRelativePath, getRefRootValue
from fxpt.fx_refSystem.log_dialog import log
from fxpt.fx_refSystem.ref_handle import RefHandle, ATTR_REF_FILENAME, REF_NODE_SUFFIX, INSTANCES_SOURCE_GROUP
from fxpt.fx_refSystem.import_save import importReference
from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_utils.watch import watch

ACTIVATION_WARNING_LIMIT = 99


# ---------------------------------------------------------------------------------------------------------------------
# misc procedures
# ---------------------------------------------------------------------------------------------------------------------

def maintainanceProcedure():
    for refNode in m.ls('*' + REF_NODE_SUFFIX, typ='reference'):
        if not m.connectionInfo(refNode + '.message', isSource=True):
            m.file(
                referenceNode=refNode,
                removeReference=True,
                force=True
            )

    instSrcGroup = '|' + INSTANCES_SOURCE_GROUP
    if m.objExists(instSrcGroup):
        if not m.listRelatives(instSrcGroup, children=True):
            m.lockNode(instSrcGroup, lock=False)
            m.delete(instSrcGroup)


def browseReference():

    globalPrefsHandler.loadPrefs()
    lastBrowsed = globalPrefsHandler.getValue(globalPrefsHandler.KEY_LAST_BROWSED_CREATE_REF) or ''

    filename = m.fileDialog2(
        dialogStyle=1,
        caption='Choose Reference Scene',
        fileFilter='Maya Scenes (*.mb; *.ma);;Maya Binary (*.mb);;Maya ASCII (*.ma);;All Files (*.*)',
        fileMode=1,
        returnFilter=False,
        startingDirectory=lastBrowsed
    )
    if not filename:
        return None

    filename = cleanupPath(filename[0])

    globalPrefsHandler.setValue(globalPrefsHandler.KEY_LAST_BROWSED_CREATE_REF, cleanupPath(os.path.dirname(filename)))
    globalPrefsHandler.savePrefs()

    return getRelativePath(filename)


def browseDir():
    globalPrefsHandler.loadPrefs()
    lastBrowsed = globalPrefsHandler.getValue(globalPrefsHandler.KEY_LAST_BROWSED_DIR) or ''

    directory = m.fileDialog2(
        dialogStyle=1,
        caption='Choose Directory',
        # fileFilter='Maya Scenes (*.mb; *.ma);;Maya Binary (*.mb);;Maya ASCII (*.ma);;All Files (*.*)',
        fileMode=3,
        returnFilter=False,
        startingDirectory=lastBrowsed
    )

    if not directory:
        return None

    directory = cleanupPath(directory[0])

    globalPrefsHandler.setValue(globalPrefsHandler.KEY_LAST_BROWSED_DIR, cleanupPath(os.path.dirname(directory)))
    globalPrefsHandler.savePrefs()

    return directory


# TODO: revise algorithm. this one is very draft.
def removeRefDuplicates(tolerance=0.001):
    import math
    from operator import attrgetter

    allHandles = getRefHandles(getWorkingRefShapes())
    duplicateHandles = []

    for rh in allHandles:
        rh.wsTranslation = m.xform(rh.refLocator.transform, q=True, ws=True, t=True)
        rh.originDistance = math.sqrt(rh.wsTranslation[0] ** 2 + rh.wsTranslation[1] ** 2 + rh.wsTranslation[2] ** 2)

    allHandles = sorted(allHandles, key=attrgetter('originDistance'))

    for i in xrange(len(allHandles)):
        rh = allHandles[i]
        for j in xrange(i + 1, len(allHandles)):
            rh2 = allHandles[j]

            # TODO: will delete different refs in the same place?
            if (rh.originDistance - rh2.originDistance) > tolerance:
                break

            # TODO: rotation and scaling?
            if distanceBetween(rh.wsTranslation, rh2.wsTranslation) <= tolerance:
                duplicateHandles.append(rh)
                break

    print 'found {} duplicates. Deleted.'.format(len(duplicateHandles)),
    m.delete([rh.refLocator.transform for rh in duplicateHandles])


def cleanupReferences():
    deactivateRefs(getAllRefHandles())


def setRefFilename(refNode, filename):
    workingFilename = filename
    reMatch = re.match(r'(.*)({.*})', workingFilename, re.IGNORECASE)
    if reMatch:
        workingFilename = reMatch.group(1)

    ext = os.path.splitext(workingFilename)[1]
    mayaFileType = 'mayaBinary' if ext == '.mb' else 'mayaAscii'

    m.file(
        filename,
        loadReference=refNode,
        typ=mayaFileType,
        options='v=0'
    )


def cleanupEmptyRefNodes():
    roReferences = set(m.ls(
        l=True,
        ro=True,
        typ='reference'
    ))

    for refNode in m.ls(l=True, references=True):

        if refNode not in roReferences:

            try:
                m.referenceQuery(refNode, filename=True, unresolvedName=True)
            except RuntimeError:
                print 'Empty reference node found:', refNode
                m.delete(refNode)
                print refNode, 'deleted.'


def makeRefsPathRelative():

    cleanupEmptyRefNodes()

    if not getRefRootValue():
        return

    for rh in getAllRefHandles():
        refFilename = rh.getRefFilename()
        relativeFilename = getRelativePath(refFilename)
        if not (refFilename.lower() == relativeFilename.lower()):
            rh.setRefFilename(relativeFilename)


def distanceBetween(firstTr, secondTr):
    return math.sqrt((firstTr[0] - secondTr[0]) ** 2
                     + (firstTr[1] - secondTr[1]) ** 2
                     + (firstTr[2] - secondTr[2]) ** 2)


gSelection = []


def saveSelection():
    global gSelection
    gSelection = m.ls(sl=True, l=True)


def restoreSelection():
    remainedNodes = [node for node in gSelection if m.objExists(node)]
    if remainedNodes:
        m.select(remainedNodes, r=True)
    else:
        m.select(cl=True)


# ---------------------------------------------------------------------------------------------------------------------
# get helpers
# ---------------------------------------------------------------------------------------------------------------------

def isRefLocatorShape(shape):
    return m.objExists('{}.{}'.format(shape, ATTR_REF_FILENAME))


def filterShapes(shapes):
    return [shape for shape in shapes if isRefLocatorShape(shape)]


def getAllRefShapes():
    return filterShapes(m.ls(l=True, typ='locator'))


def getWorkingRefShapes():
    if m.ls(sl=True, l=True, typ='dagNode'):
        locShapes = m.ls(sl=True, dag=True, l=True, typ='locator')
    else:
        locShapes = getAllRefShapes()

    return filterShapes(locShapes)


def getRefHandles(refShapes):
    res = []
    for refShape in refShapes:
        refHandle = RefHandle()
        refHandle.loadFromRefLocatorShape(refShape)
        res.append(refHandle)
    return res


def getActiveRefHandles():
    return [rh for rh in getRefHandles(getAllRefShapes()) if rh.active]


def getAllRefHandles():
    return getRefHandles(getAllRefShapes())


# ---------------------------------------------------------------------------------------------------------------------
# main procedures
# ---------------------------------------------------------------------------------------------------------------------

def createRef(refFilename):
    refHandle = RefHandle()
    refHandle.createNew(refFilename)
    return refHandle.refLocator.transform


def createRefUI():
    refFilename = browseReference()
    if refFilename:
        refTransform = createRef(refFilename)
        if refTransform and m.objExists(refTransform):
            m.select(refTransform, r=True)


def activateRefs(refHandles):
    saveSelection()

    # this cleanup deactivation cannot be done in refHandle.activate() just before instancing - maya will crash
    # the problem is in deletion of refGeom and instancing right after this procedure
    # so the solution is: first deactivate all inactive and then activate (not deactivate/activate for each ref)
    for refHandle in refHandles:
        if not refHandle.active:
            refHandle.deactivate()

    for refHandle in refHandles:
        refHandle.activate()

    restoreSelection()


def activateRefsUI(warn=True):
    refHandles = getRefHandles(getWorkingRefShapes())

    if warn:
        activationCount = len(refHandles)
        if activationCount > ACTIVATION_WARNING_LIMIT:
            if messageBoxMaya(
                    message='You are going to activate {} references.\nAre you sure?'.format(activationCount),
                    title='Confirmation',
                    icon='question',
                    button=['Ok', 'Cancel'],
                    defaultButton='Cancel',
                    cancelButton='Cancel',
                    dismissString='Cancel'
            ) != 'Ok':
                return

    activateRefs(refHandles)


def deactivateRefs(refHandles):
    saveSelection()

    for refHandle in refHandles:
        refHandle.deactivate()
    maintainanceProcedure()

    restoreSelection()


def deactivateRefsUI():
    deactivateRefs(getRefHandles(getWorkingRefShapes()))


def setReference(refHandles, refFilename):
    saveSelection()

    activeRefHandles = [rh for rh in refHandles if rh.active]

    # see activateRefs() for explanation why deactivate is not in activate() method
    for refHandle in refHandles:
        refHandle.deactivate()

    for refHandle in refHandles:
        refHandle.setRefFilename(refFilename)

    for refHandle in activeRefHandles:
        refHandle.activate()

    maintainanceProcedure()
    restoreSelection()


def setReferenceUI():
    refFilename = browseReference()
    if refFilename:
        setReference(getRefHandles(getWorkingRefShapes()), refFilename)


def retargetRefs(refHandles, targetDir):
    refFilenamesToRetarget = set([os.path.basename(rh.getRefFilename()).lower() for rh in refHandles])
    duplicatesInTargetDir = set()
    targetsDb = {}
    for root, directories, files in os.walk(targetDir):
        for f in files:
            lowCaseFilename = f.lower()
            if lowCaseFilename not in refFilenamesToRetarget:
                continue

            fullPath = cleanupPath(os.path.join(root, f))
            if lowCaseFilename in targetsDb:
                duplicatesInTargetDir.add(f)
            else:
                targetsDb[lowCaseFilename] = fullPath

    notFoundInTargetDir = set()
    rhToRetarget = []
    for rh in refHandles:
        basename = os.path.basename(rh.getRefFilename())
        basenameLower = basename.lower()

        if basenameLower in notFoundInTargetDir:
            continue

        if basenameLower not in targetsDb:
            notFoundInTargetDir.add(basename)
            continue

        rhToRetarget.append((rh, getRelativePath(targetsDb[basenameLower])))

    saveSelection()

    activeRefHandles = [rh for rh, target in rhToRetarget if rh.active]

    # see activateRefs() for explanation why deactivate is not in activate() method
    for refHandle, target in rhToRetarget:
        refHandle.deactivate()

    for refHandle, target in rhToRetarget:
        refHandle.setRefFilename(target)

    for refHandle in activeRefHandles:
        refHandle.activate()

    maintainanceProcedure()
    restoreSelection()

    # noinspection PyListCreation
    logText = list()
    if duplicatesInTargetDir:
        logText.append('Duplicates found in target directory tree for following reference(s) (retargeted to first occurence):')
        logText.extend(sorted(duplicatesInTargetDir))
    if notFoundInTargetDir:
        logText.append('')
        logText.append('Following reference(s) was not found in target directory tree (leaved intact):')
        logText.extend(sorted(notFoundInTargetDir))
    log.showLog(logText)


def retargetRefsUI():
    targetDir = browseDir()
    if targetDir:
        retargetRefs(getRefHandles(getWorkingRefShapes()), targetDir)


def importReferenceUI():
    importReference(getRefHandles(getWorkingRefShapes()))


# ---------------------------------------------------------------------------------------------------------------------
# jobs
# ---------------------------------------------------------------------------------------------------------------------

gPresaveActiveRefHandles = []


# noinspection PyUnusedLocal
def preSaveProcedure(callbackArg):
    global gPresaveActiveRefHandles
    gPresaveActiveRefHandles = getActiveRefHandles()
    deactivateRefs(gPresaveActiveRefHandles)
    makeRefsPathRelative()


# noinspection PyUnusedLocal
def postSaveProcedure(callbackArg):
    activateRefs(gPresaveActiveRefHandles)


# noinspection PyUnusedLocal
def postOpenProcedure(callbackArg):
    cleanupReferences()
    makeRefsPathRelative()
