import maya.cmds as m


def reproduceCrash():
    # m.undoInfo(state=False)

    sel = m.ls(sl=True, l=True)[0]
    oldParent = m.listRelatives(sel, fullPath=True, parent=True)[0]
    newObject = m.parent(sel, world=True)[0]
    m.parent(newObject, oldParent)
    m.delete(sel)

    # m.undoInfo(state=True)


"""
what if?

import maya.cmds as m

sel = m.ls(sl=True, l=True)[0]
sel2 = m.duplicate(sel, rr=True)[0]
newObject = m.parent(sel2, world=True)[0]
m.delete(newObject)


"""