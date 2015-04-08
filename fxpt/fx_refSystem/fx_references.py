import os
import maya.cmds as m
import maya.OpenMaya as om

from fxpt.fx_refSystem import envTools
from fxpt.fx_refSystem.miscMayaHelpers import getRelativePath, isPathRelative, messageBoxMaya, distanceBetween
from fxpt.fx_utils.utilsMaya import getLongName, getShape, getParent

ATTR_REF_NODE_MESSAGE_NAMES = ('refNodeMessage', 'refNodeMessage', 'Ref Node Message')
ATTR_REF_NODE_MESSAGE = ATTR_REF_NODE_MESSAGE_NAMES[0]

ATTR_REF_FILENAME_NAMES = ('refFilename', 'refFilename', 'Reference Filename')
ATTR_REF_FILENAME = ATTR_REF_FILENAME_NAMES[0]

INSTANCES_SOURCE_GROUP = 'refInstancesSource'

REF_LOCATOR_SUFFIX = '_refLoc'
REF_NODE_SUFFIX = '_refRN'
REF_INST_NAME = 'refGeom'

ACTIVATION_WARNING_LIMIT = 99

gSelection = []


#----------------------------------------------------------------------------------------------------------------------
# CLASS: TransformHandle
#----------------------------------------------------------------------------------------------------------------------
# noinspection PyMethodMayBeStatic
class TransformHandle(object):
    def __init__(self, transform=None, shape=None):
        if (transform is not None) and (m.objExists(transform)):
            self.transform = transform
            self.shape = getShape(transform)
        elif (shape is not None) and (m.objExists(shape)):
            self.transform = getParent(shape)
            self.shape = shape
        else:
            self.transform = None
            self.shape = None

    def __str__(self):
        return 'transform={}, shape={}'.format(self.transform, self.shape)

    def getChildren(self, allDescendants=False, typ=None):
        if typ:
            return sorted(m.listRelatives(self.transform, children=True, allDescendents=allDescendants, fullPath=True,
                                          typ=typ) or [])
        else:
            return sorted(
                m.listRelatives(self.transform, children=True, allDescendents=allDescendants, fullPath=True) or [])

    def exists(self):
        return (self.transform is not None) and (m.objExists(self.transform))


#----------------------------------------------------------------------------------------------------------------------
# CLASS: RefHandle
#----------------------------------------------------------------------------------------------------------------------
# noinspection PyMethodMayBeStatic
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
        self.refFilename = getRelativePath(m.getAttr('{}.{}'.format(refLocatorShape, ATTR_REF_FILENAME)))
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

    def generateIdString(self, refFilename):
        s = os.path.splitext(refFilename)[0]
        s = s[len(envTools.getRefRootVarNamePercent()) + 1:].replace('/', '__')
        return s.lower()

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
            m.warning('{}: {}: Reference does not exists. Activation skipped.'.format(self.refLocator.shape,
                                                                                      self.refFilename))
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
        parentAPI(inst, self.refLocator.transform)
        # m.parent(inst, self.refLocator.transform, relative=True)
        m.connectAttr(self.refNode + '.message', self.refLocator.shape + '.refNodeMessage', force=True)

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

    def refExists(self):
        return os.path.exists(os.path.expandvars(self.refFilename))

    def isTheSameAs(self, other):
        return self.idString == other.idString


#----------------------------------------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------------------------------------
def saveSelection():
    global gSelection
    gSelection = m.ls(sl=True, l=True)


def restoreSelection():
    remainedNodes = [node for node in gSelection if m.objExists(node)]
    if remainedNodes:
        m.select(remainedNodes, r=True)
    else:
        m.select(cl=True)


def nodeToMObject(node):
    selectionList = om.MSelectionList()
    selectionList.add(node)
    mObj = om.MObject()
    selectionList.getDependNode(0, mObj)
    return mObj


def parentAPI(source, target):
    mSource = nodeToMObject(source)
    mTarget = nodeToMObject(target)
    mDagMod = om.MDagModifier()
    mDagMod.reparentNode(mSource, mTarget)
    mDagMod.doIt()


def stripNamespaces(name):
    return name.split(':')[-1]


def lockTransformations(transform, visibility=True):
    attributes = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
    if visibility:
        attributes.append('.v')
    for attr in attributes:
        m.setAttr(transform + attr, lock=True)


def isRefLocatorShape(shape):
    return m.objExists('{}.{}'.format(shape, ATTR_REF_FILENAME))


def isValidRefLocatorShape(shape):
    if not isPathRelative(m.getAttr('{}.{}'.format(shape, ATTR_REF_FILENAME))):
        return False
    return True


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
    filename = m.fileDialog2(
        dialogStyle=1,
        caption='Choose Reference Scene',
        startingDirectory=envTools.getSourceDir(),
        fileFilter='Maya Scenes (*.mb; *.ma);;Maya Binary (*.mb);;Maya ASCII (*.ma);;All Files (*.*)',
        fileMode=1,
        returnFilter=False
    )
    if not filename:
        return None

    refFilename = getRelativePath(filename[0])

    if isPathRelative(refFilename):
        return refFilename
    else:
        m.warning('{}: Reference outside ref root or bad filename. Ignored.'.format(refFilename))
        return None


def filterShapes(shapes):
    refShapes = []
    for shape in shapes:
        if isRefLocatorShape(shape):
            if isValidRefLocatorShape(shape):
                refShapes.append(shape)
            else:
                m.warning('{}: Reference outside ref root or bad filename. Ignored.'.format(shape))
    return refShapes


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
    # the problem is in deletition of refGeom and instancing right after this procedure
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

    restoreSelection()


def setReferenceUI():
    refFilename = browseReference()
    if not refFilename:
        return
    setReference(getRefHandles(getWorkingRefShapes()), refFilename)


def getActiveRefHandles():
    return [rh for rh in getRefHandles(getAllRefShapes()) if rh.active]


def getAllRefHandles():
    return getRefHandles(getAllRefShapes())


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
            if (rh.originDistance - rh2.originDistance) > tolerance:
                break
            if distanceBetween(rh.wsTranslation, rh2.wsTranslation) <= tolerance:
                duplicateHandles.append(rh)
                break

    print 'found {} duplicates. Deleted.'.format(len(duplicateHandles)),
    m.delete([rh.refLocator.transform for rh in duplicateHandles])


def cleanupReferences():
    deactivateRefs(getAllRefHandles())



