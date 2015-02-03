import maya.cmds as m

from fxpt.fx_textureManager import TexNode

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

    def __init__(self):
        self.tns = []
        self.visited = set()
        # noinspection PySetFunctionToLiteral
        self.skipInRecursion = set((
            'transform',
            'groupId'
        ))

    def getTexNodes(self):
        if self.tns:
            return self.tns
        for sg in self.getAssignedSGs():
            self.tns.extend(self.findTextureNodes(sg))
        return self.tns

    def findTextureNodes(self, node):
        self.visited.add(node)
        res = []

        nodeType = m.nodeType(node)
        if nodeType in TEX_ATTRIBUTES:
            for attr in TEX_ATTRIBUTES[nodeType]:
                if m.objExists('{}.{}'.format(node, attr)):
                    res.append(TexNode.TexNode(node, attr))

        inConnections = list(set(m.listConnections(node, d=False, s=True) or []))
        for srcNode in inConnections:
            if (m.nodeType(srcNode) not in self.skipInRecursion) and (srcNode not in self.visited):
                res.extend(self.findTextureNodes(srcNode))

        return res

    def getAssignedSGs(self):
        selectedNodes = self.getSelectedNodes()
        assignedSgs = set()
        for sg in m.ls(typ='shadingEngine'):
            for member in (m.sets(sg, q=True) or []):
                if member.split('.')[0] in selectedNodes:
                    assignedSgs.add(sg)
                    break
        return assignedSgs

    # noinspection PyMethodMayBeStatic
    def getSelectedNodes(self):
        res = set(m.ls(sl=True, dag=True, ap=True))
        for s in m.ls(sl=True):
            node = s.split('.')[0]
            res.add(node)
            res.update(m.listRelatives(node, shapes=True, pa=True) or [])
        return res
