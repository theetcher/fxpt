import maya.cmds as m


def getParent(node):
    parents = m.listRelatives(node, parent=True, fullPath=True)
    if parents:
        return parents[0]
    else:
        return None


def longNameOf(node):
    if node and m.objExists(node):
        longNames = m.ls(node, l=True)
        if longNames:
            return longNames[0]


def geomMean(seq):
    return (reduce(lambda x, y: x * y, seq))**(1.0 / len(seq))


def ariMean(seq):
    return float(sum(seq)) / len(seq) if len(seq) > 0 else float('nan')
