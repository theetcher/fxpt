import maya.cmds as m
from maya.mel import eval as meval
from fxpt.fx_utils.utils_maya import getShortName


def fxCombine(merge=False):
    targets = m.ls(sl=True, l=True)

    if not targets:
        return

    parent = m.listRelatives(targets[0], p=True, pa=True)

    try:
        combineResult = m.polyUnite(targets)
    except RuntimeError:
        m.error('Invalid selection for combine operation.')
        return

    if parent:
        combineResult = m.parent(combineResult[0], parent[0])

    m.delete(combineResult[0], ch=True)

    for t in targets:
        if m.objExists(t):
            m.delete(t)

    finalObject = m.rename(combineResult[0], getShortName(targets[0]))
    m.select(finalObject)

    if merge:
        meval('performPolyMerge 0')
        m.polyOptions(finalObject, displayBorder=True, sizeBorder=4)
        m.select(finalObject)


