import maya.api.OpenMaya as om

from . import com, edge, vertex
from . import debug


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

        # for i, n in enumerate(self.meshFn.getVertexNormals(False, space=om.MSpace.kWorld)):
        #     self.vertices[i].normal = om.MVector(n)

        vertexNormals = [None] * self.meshFn.numVertices
        for pi in range(self.meshFn.numPolygons):
            polygonVertices = self.meshFn.getPolygonVertices(pi)
            for vi in polygonVertices:
                vertexNormals[vi] = self.meshFn.getFaceVertexNormal(pi, vi, space=om.MSpace.kWorld)

        for i, n in enumerate(vertexNormals):
            self.vertices[i].normal = n

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

    def process(self, curvThreshold, curvDisplayMaxValue):
        self.display(curvThreshold, curvDisplayMaxValue)

    def display(self, curvThreshold, curvDisplayMaxValue):
        colors = []
        verticesIds = []
        for v in self.vertices:
            absCurvature = abs(v.curvature)
            scaledAbsCurvature = absCurvature / curvDisplayMaxValue
            color = om.MColor((scaledAbsCurvature, scaledAbsCurvature, scaledAbsCurvature)) if absCurvature > curvThreshold else om.MColor((0.0, 1.0, 0.0))
            colors.append(color)
            verticesIds.append(v.id)

        self.meshFn.setVertexColors(colors, verticesIds)

    def _dbgDumpVertices(self):
        for p in self.vertices:
            print p

    def _dbgDebug1(self):
        # _debug
        v = self.vertices[56]
        print
        print v
        for e in v.edges:
            print e

        for eid in [459, 196]:
            e = self.edges[eid]
            print
            print e
            normDiff = e.v2.normal - e.v1.normal
            pointDiff = e.v2.point - e.v1.point
            print 'normDiff', normDiff.length()
            print 'pointDiff', pointDiff.length()
            print 'e.v1.normal', e.v1.normal
            print 'e.v2.normal', e.v2.normal

            debug.locatorByWorldPoint(e.v1.normal, name='e_{}_v1_normal'.format(eid))
            debug.locatorByWorldPoint(e.v2.normal, name='e_{}_v2_normal'.format(eid))

    def _dbgDebug2(self):
        print '---'
        for n in self.meshFn.getNormals(space=om.MSpace.kWorld):
            print n
        print

        vertexNormals = [None] * self.meshFn.numVertices
        print vertexNormals

        for pi in range(self.meshFn.numPolygons):
            polygonVertices = self.meshFn.getPolygonVertices(pi)
            for vi in polygonVertices:
                vertexNormals[vi] = self.meshFn.getFaceVertexNormal(pi, vi, space=om.MSpace.kWorld)

        print '---'
        for n in vertexNormals:
            print n
        print
