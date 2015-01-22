import maya.cmds as m

from fxpt.fx_textureManager import TexNode


class MayaSceneHarvester(object):

    texAttributes = {
        'file': [
            'fileTextureName'
        ],
        'mentalrayTexture': [
            'fileTextureName'
        ]
    }

    def __init__(self):
        pass

    def getTexNodes(self):
        texNodes = []
        for nodeType in self.__class__.texAttributes:
            for node in m.ls(l=True, typ=nodeType):
                for attr in self.__class__.texAttributes[nodeType]:
                    if m.objExists('{}.{}'.format(node, attr)):
                        texNodes.append(TexNode.TexNode(node, attr))

        return texNodes
