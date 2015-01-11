import os

import maya.cmds as m
from fxpt.fx_textureManager.com import cleanupPath


# noinspection PyAttributeOutsideInit
class TexNode(object):

    def __init__(self, node, attr):
        self.setNode(node)
        self.setAttr(attr)

    def __str__(self):
        return 'TexNode: {}'.format(self.getFullAttrName())

    def setNode(self, node):
        self.node = node

    def getNode(self):
        return self.node

    def setAttr(self, attr):
        self.attr = attr

    def getAttr(self):
        return self.attr

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

    def fileExists(self):
        fullPath = os.path.expandvars(self.getAttrValue())
        if os.path.basename(fullPath):
            return os.path.exists(fullPath)
        else:
            return False
