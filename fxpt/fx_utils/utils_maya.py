import maya.cmds as m
import maya.api.OpenMaya as om


def getLongName(node):
    if node and m.objExists(node):
        return m.ls(node, long=True)[0]


def getShortName(node):
    if node:
        return node.split('|')[-1]


def getNodeRelatives(node, parent=False, children=False, shapes=False, typ=None):
    if m.objExists(node):
        if typ:
            return m.listRelatives(node, fullPath=True, parent=parent, children=children, shapes=shapes, typ=typ)
        else:
            return m.listRelatives(node, fullPath=True, parent=parent, children=children, shapes=shapes)


def getParent(node):
    parents = getNodeRelatives(node, parent=True)
    if parents:
        return parents[0]


def getChildTransforms(node):
    return getNodeRelatives(node, children=True, typ='transform')


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

    if absolute:
        srcFnDependencyNode = om.MFnDependencyNode(mSource)
        worldMatrixPlug = srcFnDependencyNode.findPlug('worldMatrix', False).elementByLogicalIndex(0)
        matrixMObj = worldMatrixPlug.asMObject()
        fnMatrixData = om.MFnMatrixData(matrixMObj)

        srcWMtx = fnMatrixData.transformation()

    mDagMod = om.MDagModifier()
    if target:
        mTarget = nodeToMObject(target)
        mDagMod.reparentNode(mSource, mTarget)
    else:
        mDagMod.reparentNode(mSource)
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


def opFlagEraser():
    selection = m.ls(sl=True, l=True)

    if selection:
        targets = m.ls(sl=True, l=True, dag=True, ap=True, typ='mesh')
    else:
        targets = m.ls(l=True, typ='mesh')

    if not targets:
        return

    counter = 0
    for t in targets:
        opAttr = t + '.opposite'
        op = m.getAttr(opAttr)
        if op:
            counter += 1
            m.polyNormal(t, nm=0, ch=False)
            m.setAttr(opAttr, False)

    print '{} opposite flag(s) erased.'.format(counter),

    m.select(selection, r=True)


def freezeRotationToWorld():

    targets = m.ls(sl=True, l=True)

    for t in targets:
        node = t
        shortName = getShortName(t)
        parent = m.listRelatives(t, p=True, pa=True)
        if parent:
            node = m.parent(t, w=True)[0]
        m.makeIdentity(node, apply=True, t=False, r=True, s=False)
        if parent:
            node = m.parent(node, parent[0])[0]
            if getShortName(node) != shortName:
                m.rename(node, shortName)


def unfreezeTranslation():

    targets = m.ls(sl=True, l=True, tr=True)

    if not targets:
        return

    for t in targets:
        m.makeIdentity(t, apply=True, t=True, r=False, s=False)
        m.move(0, 0, 0, t, ws=True, rpr=True)
        translate = [-1 * tr for tr in m.getAttr(t + '.translate')[0]]
        m.makeIdentity(t, apply=True, t=True, r=False, s=False)
        m.setAttr(t + '.translate', *translate)


def fxSeparate():
    selection = m.ls(sl=True, long=True, tr=True)
    for s in selection:
        try:
            m.polySeparate(s, ch=False)
        except RuntimeError:
            m.warning('Mesh ignored because has only one piece: {}'.format(s))
