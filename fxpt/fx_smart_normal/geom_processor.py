from math import pi

import maya.api.OpenMaya as om

from . import com, edge, vertex


# noinspection PyArgumentList
class GeomProcessor(object):
    """
    :type meshTransform: str
    :type dagPath: om.MDagPath
    :type meshFn: om.MFnMesh
    :type vertices: list[vertex.Vertex]
    :type edges: list[edge.Edge]
    """

    def __init__(self, meshTransform):
        self.meshTransform = meshTransform
        self.dagPath = self.getDagPath()
        self.meshFn = self.createMeshFn()
        self.vertices = []
        self.edges = []

        self.harvestData()

    def getDagPath(self):
        selList = om.MSelectionList()
        selList.add(com.longNameOf(self.meshTransform))
        return selList.getDagPath(0)

    def createMeshFn(self):
        return om.MFnMesh(self.dagPath)

    def harvestData(self):
        self.harvestPoints()
        self.harvestEdges()
        self.calculateVtxCurvatures()

    def harvestPoints(self):
        for i, p in enumerate(self.meshFn.getPoints(space=om.MSpace.kWorld)):
            vtx = vertex.Vertex(i)
            vtx.point = p
            self.vertices.append(vtx)

        for i, n in enumerate(self.meshFn.getVertexNormals(False, space=om.MSpace.kWorld)):
            self.vertices[i].normal = om.MVector(n)

    def harvestEdges(self):
        for i in xrange(self.meshFn.numEdges):
            iv1, iv2 = self.meshFn.getEdgeVertices(i)
            e = edge.Edge(i, self.vertices[iv1], self.vertices[iv2])
            self.edges.append(e)

            self.vertices[iv1].edges.append(e)
            self.vertices[iv2].edges.append(e)

    def calculateVtxCurvatures(self):
        for v in self.vertices:
            v.calculateCurvature()
            print v
