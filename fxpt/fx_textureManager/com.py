import maya.cmds as m


def getShadingGroups(node, visited):
    sgs = set()
    visited.add(node)
    outConnections = m.listConnections(node, s=False, d=True)
    if outConnections:
        for destinationNode in outConnections:
            if m.objectType(destinationNode, isType='shadingEngine'):
                sgs.add(destinationNode)
            else:
                sgs.update(getShadingGroups(destinationNode, visited))
    return sgs

