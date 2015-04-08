import maya.cmds as m


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


