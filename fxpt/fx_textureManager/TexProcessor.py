import maya.cmds as m

from fxpt.fx_textureManager import TexNode

#TODO: delete transform from this list at the end and cleanup tests
texAttributes = {
    'file': [
        'fileTextureName'
    ],
    'transform': [
        'texture',
        'texture1',
        'texture2'
    ]
}


class TexProcessor(object):

    def __init__(self):
        self.texNodes = []

    def collectTexNodes(self):
        self.texNodes = []
        for nodeType in texAttributes:
            for node in m.ls(l=True, typ=nodeType):
                for attr in texAttributes[nodeType]:
                    if m.objExists('{}.{}'.format(node, attr)):
                        self.texNodes.append(TexNode.TexNode(node, attr))

    def getTexNodes(self):
        return self.texNodes