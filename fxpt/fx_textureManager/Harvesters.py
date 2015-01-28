import maya.cmds as m

from fxpt.fx_textureManager import TexNode

from fxpt.fx_utils.watch import watch


TEX_ATTRIBUTES = {
    'file': [
        'fileTextureName'
    ],
    'mentalrayTexture': [
        'fileTextureName'
    ]
}


class HarvesterBase(object):

    def getTexNodes(self):
        raise NotImplementedError('Call to abstract method.')


class MayaSceneHarvester(HarvesterBase):

    def getTexNodes(self):
        texNodes = []
        for nodeType in TEX_ATTRIBUTES:
            for node in m.ls(l=True, typ=nodeType):
                for attr in TEX_ATTRIBUTES[nodeType]:
                    if m.objExists('{}.{}'.format(node, attr)):
                        texNodes.append(TexNode.TexNode(node, attr))

        return texNodes


class MayaSelectionHarvester(HarvesterBase):

    def getTexNodes(self):
        watch(self.getAssignedSGs())

    def getAssignedSGs(self):
        selectedNodes = self.getSelectedNodes()
        assignedSgs = set()
        for sg in m.ls(typ='shadingEngine'):
            for member in m.sets(sg, q=True):
                if member.split('.')[0] in selectedNodes:
                    assignedSgs.add(sg)
                    break
        return assignedSgs

    # noinspection PyMethodMayBeStatic
    def getSelectedNodes(self):
        res = set()
        for s in m.ls(sl=True):
            node = s.split('.')[0]
            res.add(node)
            res.update(m.listRelatives(node, shapes=True, pa=True) or [])
        return res
