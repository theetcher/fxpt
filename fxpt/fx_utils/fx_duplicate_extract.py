from collections import defaultdict

import maya.cmds as m
from maya.mel import eval as meval


def doDuplicateExtract():
    selection = m.ls(sl=True, l=True)
    if not selection:
        raise RuntimeError('Bad selection. Select some polygons.')

    components = defaultdict(list)
    for s in selection:
        split = s.split('.')
        if (len(split) != 2) or (not split[1].startswith('f[')):
            raise RuntimeError('Bad selection. Only polygons allowed: {}'.format(s))
        components[split[0]].append(split[1])

    originalObjects = components.keys()
    newObjects = []
    wholeDuplicatedObjects = []

    for obj in originalObjects:
        dup = m.duplicate(obj)[0]
        newObjects.append(dup)

        newSelection = [dup + '.' + c for c in components[obj]]
        m.select(newSelection, r=True)
        meval('InvertSelection')

        if m.ls(sl=True):
            m.delete()
        else:
            wholeDuplicatedObjects.append(obj)

    m.select(selection, r=True)

    return newObjects, wholeDuplicatedObjects


def run(deleteOriginals=True):
    newObjects, wholeDuplicatedObjects = doDuplicateExtract()

    if deleteOriginals:
        m.delete()
        if wholeDuplicatedObjects:
            m.delete(wholeDuplicatedObjects)

    meval('changeSelectMode -object')
    m.select(newObjects, r=True)
