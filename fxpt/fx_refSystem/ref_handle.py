import os
import re

from maya import cmds as m

from fxpt.fx_refSystem.com import REF_ROOT_VAR_NAME, REF_ROOT_VAR_NAME_P, isPathRelative
from fxpt.fx_refSystem.transform_handle import TransformHandle
from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_utils.utilsMaya import getLongName, getShape, getParent, parentAPI


ATTR_REF_FILENAME_NAMES = ('refFilename', 'refFilename', 'Reference Filename')
ATTR_REF_FILENAME = ATTR_REF_FILENAME_NAMES[0]

ATTR_REF_NODE_MESSAGE_NAMES = ('refNodeMessage', 'refNodeMessage', 'Ref Node Message')
ATTR_REF_NODE_MESSAGE = ATTR_REF_NODE_MESSAGE_NAMES[0]

ATTR_REF_SOURCE_PATH_NAMES = ('refSource', 'refSource', 'Reference Source')
ATTR_REF_SOURCE_PATH = ATTR_REF_SOURCE_PATH_NAMES[0]

REF_NODE_SUFFIX = '_refRN'
REF_LOCATOR_SUFFIX = '_refLoc'
REF_INST_NAME = 'refGeom'

INSTANCES_SOURCE_GROUP = 'refInstancesSource'


class RefHandle(object):
    def __init__(self):
        self.refFilename = None
        self.idString = None
        self.refShortName = None
        self.refLocator = None
        self.annotation = None
        self.refNode = None
        self.instanceSource = None
        self.active = False

    def __str__(self):
        return 'refFilename={}, idString={}, refShortName={}, refLocator=[{}], annotation=[{}],' \
               'refNode={}, instanceSource={}, active={}' \
            .format(
                self.refFilename,
                self.idString,
                self.refShortName,
                self.refLocator,
                self.annotation,
                self.refNode,
                self.instanceSource,
                self.active,
            )

    def loadFromRefLocatorShape(self, refLocatorShape):
        self.refFilename = cleanupPath(m.getAttr('{}.{}'.format(refLocatorShape, ATTR_REF_FILENAME)))
        self.idString = self.generateIdString(self.refFilename)
        self.refShortName = self.generateShortName(self.refFilename)
        self.refLocator = TransformHandle(shape=refLocatorShape)
        self.setAnnotation(self.refShortName)
        self.refNode = self.idString + REF_NODE_SUFFIX
        self.instanceSource = '|{}|{}'.format(INSTANCES_SOURCE_GROUP, self.idString)
        self.active = self.getActiveStateFromMaya()

    def createNew(self, refFilename):
        refLocatorTr = m.spaceLocator(p=(0, 0, 0))[0]
        refLocatorTr = getLongName(m.rename(refLocatorTr, self.generateShortName(refFilename) + REF_LOCATOR_SUFFIX))
        refLocatorSh = getShape(refLocatorTr)

        m.addAttr(
            refLocatorSh,
            at='message',
            shortName=ATTR_REF_NODE_MESSAGE_NAMES[0],
            longName=ATTR_REF_NODE_MESSAGE_NAMES[1],
            niceName=ATTR_REF_NODE_MESSAGE_NAMES[2]
        )

        m.addAttr(
            refLocatorSh,
            dt='string',
            shortName=ATTR_REF_FILENAME_NAMES[0],
            longName=ATTR_REF_FILENAME_NAMES[1],
            niceName=ATTR_REF_FILENAME_NAMES[2]
        )

        m.setAttr('{}.{}'.format(refLocatorSh, ATTR_REF_FILENAME), refFilename, typ='string')

        self.loadFromRefLocatorShape(refLocatorSh)

    # noinspection PyMethodMayBeStatic
    def generateIdString(self, refFilename):
        s = os.path.splitext(refFilename)[0]
        if isPathRelative(refFilename):
            s = REF_ROOT_VAR_NAME + s[len(REF_ROOT_VAR_NAME_P):]
        return re.sub('[^0-9a-zA-Z_]+', '__', s).lower()

    # noinspection PyMethodMayBeStatic
    def generateShortName(self, longFilename):
        return os.path.splitext(os.path.basename(longFilename))[0]

    def getActiveStateFromMaya(self):
        if not m.objExists(self.refNode):
            return False
        return m.isConnected(self.refNode + '.message', self.refLocator.shape + '.' + ATTR_REF_NODE_MESSAGE)

    def getAnnotationTransformHandle(self):
        if self.isValid():
            annotationShapes = self.refLocator.getChildren(allDescendants=True, typ='annotationShape')
            if len(annotationShapes) == 1:
                return TransformHandle(shape=annotationShapes[0])
            else:
                return None

    def isValid(self):
        return (self.refLocator is not None) and (self.refLocator.exists())

    def setAnnotation(self, text):
        if (self.annotation is None) or (not self.annotation.exists()):
            self.annotation = self.getAnnotationTransformHandle()
        if self.annotation is None:
            self.createAnnotation()
        m.setAttr(self.annotation.shape + '.text', text, typ='string')

    def createAnnotation(self):
        if not self.isValid():
            return

        annotationShapes = self.refLocator.getChildren(allDescendants=True, typ='annotationShape')
        for s in annotationShapes:
            m.delete(getParent(s))

        annotationSh = m.annotate(self.refLocator.transform, p=(0, -0.5, 0))
        annotationTr = getParent(annotationSh)
        annotationTr = m.parent(annotationTr, self.refLocator.transform, relative=True)[0]
        lockTransformations(annotationTr)
        self.annotation = TransformHandle(transform=getLongName(annotationTr))

        m.setAttr(self.annotation.shape + '.displayArrow', False)
        m.setAttr(self.annotation.transform + '.overrideEnabled', True)
        m.setAttr(self.annotation.transform + '.overrideDisplayType', 2)

    def activate(self):
        if self.active:
            return

        if not self.refExists():
            m.warning('{}: {}: Reference does not exists. Activation skipped.'.format(self.refLocator.shape, self.refFilename))
            return

        if not m.objExists(self.instanceSource):
            self.createRefSource()

        m.instance(
            self.instanceSource,
            name=REF_INST_NAME
        )

        inst = '|{}|{}'.format(INSTANCES_SOURCE_GROUP, REF_INST_NAME)
        m.setAttr(inst + '.overrideEnabled', True)
        m.setAttr(inst + '.overrideDisplayType', 2)
        lockTransformations(inst, visibility=True)
        parentAPI(inst, self.refLocator.transform, absolute=False)
        # m.parent(inst, self.refLocator.transform, relative=True)
        m.connectAttr(self.refNode + '.message', self.refLocator.shape + '.refNodeMessage', force=True)

        self.active = True

    def importRef(self):

        if not self.refExists():
            m.warning('{}: {}: Reference does not exists. Import skipped.'.format(self.refLocator.shape, self.refFilename))
            return

        m.instance(
            self.instanceSource,
            name=REF_INST_NAME
        )

        inst = '|{}|{}'.format(INSTANCES_SOURCE_GROUP, REF_INST_NAME)
        m.setAttr(inst + '.overrideEnabled', True)
        m.setAttr(inst + '.overrideDisplayType', 2)
        lockTransformations(inst, visibility=True)
        parentAPI(inst, self.refLocator.transform, absolute=False)
        # m.parent(inst, self.refLocator.transform, relative=True)

        self.active = True

    def createRefSource(self):
        if m.objExists(self.refNode):
            m.file(
                referenceNode=self.refNode,
                removeReference=True,
                force=True
            )
        fileType = 'mayaAscii' if self.refFilename.endswith('.ma') else 'mayaBinary'
        m.file(
            self.refFilename,
            reference=True,
            typ=fileType,
            referenceNode=self.refNode,
            groupReference=True,
            groupName=self.idString,
            mergeNamespacesOnClash=False,
            namespace=self.refShortName,
            options='v=0;',
        )

        instSrcGroup = '|' + INSTANCES_SOURCE_GROUP
        if not m.objExists(instSrcGroup):
            m.createNode('unknownTransform', name=INSTANCES_SOURCE_GROUP, skipSelect=True)

            # m.group(empty=True, name=INSTANCES_SOURCE_GROUP)
            m.setAttr(instSrcGroup + '.v', False, lock=True)
            # m.lockNode(instSrcGroup, lock=True)

        m.parent('|' + self.idString, instSrcGroup)

    def deactivate(self):
        refGeom = self.refLocator.getChildren()
        for rg in refGeom:
            if stripNamespaces(rg.split('|')[-1]).startswith(REF_INST_NAME):
                m.delete(rg)
        if self.getActiveStateFromMaya():
            m.disconnectAttr(self.refNode + '.message', self.refLocator.shape + '.refNodeMessage')
        self.active = False

    def setRefFilename(self, refFilename):
        m.setAttr('{}.{}'.format(self.refLocator.shape, ATTR_REF_FILENAME), refFilename, typ='string')
        self.loadFromRefLocatorShape(self.refLocator.shape)

    def getRefFilename(self):
        return cleanupPath(self.refFilename)

    def refExists(self):
        return os.path.exists(os.path.expandvars(self.refFilename))


def lockTransformations(transform, visibility=True):
    attributes = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
    if visibility:
        attributes.append('.v')
    for attr in attributes:
        m.setAttr(transform + attr, lock=True)


def stripNamespaces(name):
    return name.split(':')[-1]
