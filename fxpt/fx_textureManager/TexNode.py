import maya.cmds as m
from fxpt.fx_utils.utils import pathToSlash


# noinspection PyAttributeOutsideInit
class TexNode(object):

    def __init__(self, node, attr):
        self.setNode(node)
        self.setAttr(attr)

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
        slashedPath = pathToSlash(m.getAttr(self.getFullAttrName()))
        if slashedPath.startswith('//'):
            return '//{}'.format(slashedPath[2:].replace('//', '/'))
        else:
            return slashedPath.replace('//', '/')
