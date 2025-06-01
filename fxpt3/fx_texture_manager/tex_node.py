import os

import maya.cmds as m

from fxpt3.fx_texture_manager.com import cleanupPath

# noinspection PySetFunctionToLiteral
IGNORED_OBJECT_TYPES = set([
    'defaultShaderList',
    'defaultTextureList'
])
IGNORED_OBJECTS = set()
for t in IGNORED_OBJECT_TYPES:
    IGNORED_OBJECTS.update(m.ls(typ=t))

SHADING_ENGINE_TYPE = 'kShadingEngine'


def getShadingGroups(node, visited):
    sgs = set()
    visited.add(node)
    outConnections = m.listConnections(node, s=False, d=True)
    if outConnections:
        for destinationNode in outConnections:
            if destinationNode not in visited:
                if m.nodeType(destinationNode, apiType=True) == SHADING_ENGINE_TYPE:
                    sgs.add(destinationNode)
                else:
                    sgs.update(getShadingGroups(destinationNode, visited))
    return sgs


class TexNode(object):

    def __init__(self, node, attr):
        self.node = None
        self.attr = None
        self.sgs = None

        self.setNode(node)
        self.setAttr(attr)
        self.setSgs()

    def __str__(self):
        return f'TexNode: {self.getFullAttrName()}: {self.getAttrValue()}'

    def __eq__(self, other):
        return self.getAttrValue() == other.getAttrValue()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.getAttrValue() < other.getAttrValue()

    def __le__(self, other):
        return self.getAttrValue() <= other.getAttrValue()

    def __gt__(self, other):
        return self.getAttrValue() > other.getAttrValue()

    def __ge__(self, other):
        return self.getAttrValue() >= other.getAttrValue()

    def setNode(self, node):
        self.node = node

    def getNode(self):
        return self.node

    def setAttr(self, attr):
        self.attr = attr

    def getAttr(self):
        return self.attr

    def setSgs(self):
        self.sgs = getShadingGroups(self.node, set(IGNORED_OBJECTS))

    def getSgs(self):
        return self.sgs

    def isAssigned(self):
        for sg in self.sgs:
            if m.sets(sg, q=True):
                return True
        return False

    def getFullAttrName(self):
        return '{}.{}'.format(self.node, self.attr)

    def getAttrValue(self):
        slashedPath = cleanupPath(m.getAttr(self.getFullAttrName()))
        if slashedPath.startswith('//'):
            return '//{}'.format(slashedPath[2:].replace('//', '/'))
        else:
            return slashedPath.replace('//', '/')

    def setAttrValue(self, value):
        m.setAttr(self.getFullAttrName(), value, typ='string')

    def nodeAttrExists(self):
        return m.objExists(self.getFullAttrName())

    def fileExists(self):
        fullPath = os.path.expandvars(self.getAttrValue())
        if os.path.basename(fullPath):
            return os.path.exists(fullPath)
        else:
            return False
