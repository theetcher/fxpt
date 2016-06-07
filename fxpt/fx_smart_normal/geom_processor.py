import maya.api.OpenMaya as om
import maya.OpenMaya as om_

from . import com, components
from . import debug


# noinspection PyArgumentList
class GeomProcessor(object):
    """
    :type meshTransform: str
    :type dagPath: om.MDagPath
    :type dagPath_: om_.MDagPath
    :type meshFn: om.MFnMesh
    :type vertices: list[components.Vertex]
    :type edges: list[components.Edge]
    :type polygons: list[components.Polygon]
    :type params: fxpt.fx_smart_normal.ui.Parameters
    """

    def __init__(self, meshTransform):
        self.meshTransform = meshTransform
        self.dagPath = self.getDagPath()
        self.dagPath_ = self.getDagPath_()
        self.meshFn = self.createMeshFn()
        self.vertices = []
        self.edges = []
        self.polygons = []

        self.params = None

        self.harvestData()

    def getDagPath(self):
        selList = om.MSelectionList()
        selList.add(com.longNameOf(self.meshTransform))
        return selList.getDagPath(0)

    def getDagPath_(self):
        selList = om_.MSelectionList()
        selList.add(com.longNameOf(self.meshTransform))
        dagPath = om_.MDagPath()
        selList.getDagPath(0, dagPath)
        return dagPath

    def createMeshFn(self):
        return om.MFnMesh(self.dagPath)

    def harvestData(self):
        self.harvestVertices()
        self.harvestEdges()
        self.harvestPolygons()
        self.calculateVtxCurvatures()

    def harvestVertices(self):
        for iv, v in enumerate(self.meshFn.getPoints(space=om.MSpace.kWorld)):
            vtx = components.Vertex(iv)
            vtx.point = v
            self.vertices.append(vtx)

        # verticesIds maps 1:1 to normalIds and normals without use of polygonIds only if 1 vertex = 1 normal (my case)
        normals = self.meshFn.getNormals(space=om.MSpace.kWorld)
        _, normalIds = self.meshFn.getNormalIds()
        _, verticesIds = self.meshFn.getVertices()
        for i, iv in enumerate(verticesIds):
            normalIndex = normalIds[i]
            normal = om.MVector(normals[normalIndex])
            v = self.vertices[iv]
            v.normalId = normalIndex
            v.normal = normal

    def harvestEdges(self):
        for ie in xrange(self.meshFn.numEdges):
            iv1, iv2 = self.meshFn.getEdgeVertices(ie)
            e = components.Edge(ie, self.vertices[iv1], self.vertices[iv2])
            self.edges.append(e)

            self.vertices[iv1].edges.add(e)
            self.vertices[iv2].edges.add(e)

    def harvestPolygons(self):
        for ip in xrange(self.meshFn.numPolygons):
            p = components.Polygon(ip)
            p.normal = self.meshFn.getPolygonNormal(ip)
            self.polygons.append(p)
            for iv in self.meshFn.getPolygonVertices(ip):
                v = self.vertices[iv]
                p.vertices.add(v)
                v.polygons.add(p)

        for p in self.polygons:
            for v in p.vertices:
                for e in v.edges:
                    if e.v1 in p.vertices and e.v2 in p.vertices:
                        p.edges.add(e)
                        e.polygons.add(p)

        msu = om_.MScriptUtil()
        areaPtr = msu.asDoublePtr()
        pIter = om_.MItMeshPolygon(self.dagPath_)
        while not pIter.isDone():
            pIter.getArea(areaPtr, om_.MSpace.kWorld)
            self.polygons[pIter.index()].area = msu.getDouble(areaPtr)
            pIter.next()

        self.validateEdges()
        self.calculateEdgeAngles()

    def calculateVtxCurvatures(self):
        for v in self.vertices:
            v.calculateCurvature()

    def calculateEdgeAngles(self):
        for v in self.edges:
            v.calculateEdgeAngle()

    def validateEdges(self):
        for e in self.edges:
            assert 0 < len(e.polygons) < 3, '{} has edge #{} with {} polygons connected. Maximum 2 allowed (manifold surfaces).'.format(
                self.meshTransform, e.id, len(e.polygons))

    def process(self):
        self.display()

        newNormals = self.meshFn.getNormals(space=om.MSpace.kWorld)

        for v in self.vertices:
            if not v.isRougher(self.params.curveThresh):
                continue
            newNormals[v.normalId] = self.calculateNewNormal(v)

        self.meshFn.setNormals(newNormals)

    def calculateNewNormal(self, v):
        """
        :type v: components.Vertex
        """
        areas = {}
        for polygon in v.polygons:
            area = 0.0
            polySet = self.getGrownPolygons(polygon)

        return om.MFloatVector(0, 1, 0)

    def getGrownPolygons(self, poly):
        grownPolygons = {poly}
        newFrontPolygons = {poly}
        while True:
            grown = False
            frontPolygons = newFrontPolygons
            newFrontPolygons = set()
            for poly in frontPolygons:
                for edge in poly.edges:
                    if edge.edgeAngle < self.params.growAngle:
                        otherPoly = edge.otherPoly(poly)
                        if otherPoly is None:
                            continue
                        else:
                            if otherPoly not in grownPolygons:
                                newFrontPolygons.add(otherPoly)
                                grownPolygons.add(otherPoly)
                                grown = True
            if not grown:
                break
        return grownPolygons

    def display(self):
        colors = []
        verticesIds = []
        for v in self.vertices:
            scaledAbsCurvature = v.absCurvature / self.params.curveScale
            color = om.MColor((scaledAbsCurvature, scaledAbsCurvature, scaledAbsCurvature)) if v.isRougher(self.params.curveThresh) else om.MColor((0.0, 1.0, 0.0))
            colors.append(color)
            verticesIds.append(v.id)

        self.meshFn.setVertexColors(colors, verticesIds)

    @staticmethod
    def _dbgDumpList(l):
        if not l:
            print []
        else:
            for i, x in enumerate(l):
                print '#{}: {}'.format(i, str(x))
                # print type(l)

    def _dbgDebug1(self):
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

        for pi in xrange(self.meshFn.numPolygons):
            polygonVertices = self.meshFn.getPolygonVertices(pi)
            for vi in polygonVertices:
                vertexNormals[vi] = self.meshFn.getFaceVertexNormal(pi, vi, space=om.MSpace.kWorld)

        print '---'
        for n in vertexNormals:
            print n
        print

    def _dbgDebug3(self):
        print
        print
        print '>>> dump vertices'
        self._dbgDumpList(self.vertices)

        print '>>> meshFn.getNormals():'
        self._dbgDumpList(self.meshFn.getNormals(space=om.MSpace.kWorld))

        print '>>> meshFn.getNormalIds():'
        print self.meshFn.getNormalIds()

        print '>>> meshFn.getVertices():'
        print self.meshFn.getVertices()

        print '>>> polygon vertices:'
        for p in xrange(self.meshFn.numPolygons):
            print self.meshFn.getPolygonVertices(p)

        print '>>> setNormals()'
        self.meshFn.setNormals([om.MFloatVector(1, 0, 0), om.MFloatVector(0, 1, 0)], space=om.MSpace.kWorld)

        print '>>> meshFn.getNormals():'
        self._dbgDumpList(self.meshFn.getNormals(space=om.MSpace.kWorld))

        print '>>> meshFn.getNormalIds():'
        print self.meshFn.getNormalIds()

        print '>>> meshFn.getVertices():'
        print self.meshFn.getVertices()

        print '>>> polygon vertices:'
        for p in xrange(self.meshFn.numPolygons):
            print self.meshFn.getPolygonVertices(p)

        print '>>> dump vertices'
        self._dbgDumpList(self.vertices)
