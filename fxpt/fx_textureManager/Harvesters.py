import maya.cmds as m

from fxpt.fx_textureManager import TexNode

#TODO: mentalrayTexture as an example of other texture type.

class MayaSceneHarvester(object):

    #TODO: delete transform from this list at the end and cleanup tests
    texAttributes = {
        'file': [
            'fileTextureName'
        ],
        'lambert': [
            'textureFile',
            'textureFile1'
        ],
        'transform': [
            'texture',
            'texture1',
            'texture2'
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
