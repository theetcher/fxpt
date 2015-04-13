import maya.cmds as m
import maya.api.OpenMaya as om


def getLongName(node):
    if node and m.objExists(node):
        return m.ls(node, long=True)[0]


def getShortName(node):
    if node:
        return node.split('|')[-1]


def getNodeRelatives(node, parent=False, shapes=False):
    if m.objExists(node):
        return m.listRelatives(node, fullPath=True, parent=parent, shapes=shapes)


def getParent(node):
    parents = getNodeRelatives(node, parent=True)
    if parents:
        return parents[0]


def getShape(node):
    shapes = getNodeRelatives(node, shapes=True)
    if shapes:
        return shapes[0]


def nodeToMObject(node):
    selectionList = om.MSelectionList()
    selectionList.add(node)
    return selectionList.getDependNode(0)


def parentAPI(source, target, absolute=True):
    # TODO: implement undo
    mSource = nodeToMObject(source)
    mTarget = nodeToMObject(target)

    if absolute:
        srcFnDependencyNode = om.MFnDependencyNode(mSource)
        worldMatrixPlug = srcFnDependencyNode.findPlug('worldMatrix', False).elementByLogicalIndex(0)
        matrixMObj = worldMatrixPlug.asMObject()
        fnMatrixData = om.MFnMatrixData(matrixMObj)

        srcWMtx = fnMatrixData.transformation()

    mDagMod = om.MDagModifier()
    mDagMod.reparentNode(mSource, mTarget)
    mDagMod.doIt()

    fnDagNode = om.MFnDagNode(mSource)

    if absolute:
        srcFnTransform = om.MFnTransform(fnDagNode.getPath())
        # srcFnTransform = om.MFnTransform(mSource)
        # noinspection PyUnboundLocalVariable
        srcFnTransform.setTranslation(srcWMtx.translation(om.MSpace.kWorld), om.MSpace.kWorld)
        srcFnTransform.setRotation(srcWMtx.rotation(asQuaternion=True), om.MSpace.kWorld)
        srcFnTransform.setScale(srcWMtx.scale(om.MSpace.kWorld))
        srcFnTransform.setShear(srcWMtx.shear(om.MSpace.kWorld))

    return fnDagNode.fullPathName()
