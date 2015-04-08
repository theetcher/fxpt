import os
import re
import math
import maya.cmds as m

from fxpt.fx_refSystem import envTools
from fxpt.fx_utils.utils import pathToSlash


EXPORT_EXTENSION = '.mb'

REF_ROOT_NAME_PERCENT = '%{}%'.format(envTools.getRefRootVarName())
REF_ROOT_VALUE = envTools.getRefRoot().lower()


def isPathRelative(path):
    return path.lower().startswith(REF_ROOT_NAME_PERCENT.lower())


def getRelativePath(path):
    if not REF_ROOT_VALUE:
        return path

    pathWorking = pathToSlash(path)
    pathLower = pathToSlash(path.lower())

    if isPathRelative(pathWorking):
        return pathWorking

    if pathLower.startswith(REF_ROOT_VALUE):
        return REF_ROOT_NAME_PERCENT + pathWorking[len(REF_ROOT_VALUE):]

    return path


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

    if not REF_ROOT_VALUE:
        return

    roReferences = set(m.ls(
        l=True,
        ro=True,
        typ='reference'
    ))

    for refNode in m.ls(l=True, references=True):

        if refNode in roReferences:
            continue

        refFilename = m.referenceQuery(refNode, filename=True, unresolvedName=True).replace('\\', '/')
        relativeFilename = getRelativePath(refFilename)
        if not (refFilename.lower() == relativeFilename.lower()):
            setRefFilename(refNode, relativeFilename)


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


def distanceBetween(firstTr, secondTr):
    return math.sqrt((firstTr[0] - secondTr[0]) ** 2
                     + (firstTr[1] - secondTr[1]) ** 2
                     + (firstTr[2] - secondTr[2]) ** 2)

