from math import pi

from . import com


class Vertex(object):
    """
    :type id: int
    :type point: maya.api.OpenMaya.MPoint
    :type normal: maya.api.OpenMaya.MVector
    :type normalId: int
    :type curvature: float
    :type absCurvature: float
    :type edges: set[Edge]
    :type polygons: set[Polygon]
    """
    def __init__(self, vtxId):
        self.id = vtxId
        self.point = None
        self.normal = None
        self.normalId = None
        self.curvature = None
        self.absCurvature = None
        self.edges = set()
        self.polygons = set()

    def __str__(self):
        return 'vertex({}): point={}, normal={}, normalId={}, curvature={}, polygons=({}), edges=({})'.format(
            self.id, self.point, self.normal, self.normalId, self.curvature, ', '.join([str(p.id) for p in self.polygons]), ', '.join([str(e.id) for e in self.edges])
        )

    def calculateCurvature(self):
        self.curvature = com.ariMean([abs(e.curvature) for e in self.edges])
        self.absCurvature = abs(self.curvature)

    def isRougher(self, curvature):
        return self.absCurvature > curvature


class Edge(object):
    """
    :type id: int
    :type v1: Vertex
    :type v2: Vertex
    :type p1: Polygon
    :type p2: Polygon
    :type polygons: set[Polygon]
    :type curvature: float
    :type edgeAngle: float
    """
    def __init__(self, edgeId, v1, v2):
        self.id = edgeId
        self.v1 = v1
        self.v2 = v2
        self.p1 = None
        self.p2 = None
        self.polygons = set()
        self.curvature = None
        self.edgeAngle = 0.0
        self.calculateCurvature()

    def __str__(self):
        return 'edge({}): v1={}, v2={}, curvature={}, edgeAngle={}, polygons=({})'.format(
            self.id, self.v1.id, self.v2.id, self.curvature, self.edgeAngle, ', '.join([str(p.id) for p in self.polygons])
        )

    def calculateCurvature(self):
        normDiff = self.v2.normal - self.v1.normal
        pointDiff = self.v2.point - self.v1.point
        self.curvature = (normDiff * pointDiff) / (pointDiff * pointDiff)

    def calculateEdgeAngle(self):
        polyList = list(self.polygons)
        if len(polyList) == 1:
            self.p1 = polyList[0]
            self.edgeAngle = 0.0
        else:
            self.p1, self.p2 = polyList
            self.edgeAngle = self.p1.normal.angle(self.p2.normal) * 180 / pi

    def otherPoly(self, p):
        return self.p1 if p is not self.p1 else self.p2


class Polygon(object):
    """
    :type id: int
    :type normal: maya.api.OpenMaya.MVector
    :type area: float
    :type vertices: set[Vertex]
    :type edges: set[Edge]
    """

    def __init__(self, polyId):
        self.id = polyId
        self.normal = None
        self.area = None
        self.vertices = set()
        self.edges = set()

    def __str__(self):
        return 'polygon({}): normal={}, area={}, vertices=({}), edges=({})'.format(
            self.id, self.normal, self.area, ', '.join([str(p.id) for p in self.vertices]), ', '.join([str(p.id) for p in self.edges])
        )


class PolySet(object):
    """
    :type normal: maya.api.OpenMaya.MVector
    :type area: float
    :type polygons: set[Polygon]
    """
    def __init__(self, masterPolygon):
        self.normal = masterPolygon.normal
        self.area = masterPolygon.area
        self.polygons = {masterPolygon}

    def __str__(self):
        return 'polyset: normal={}, area={}, polygons=({})'.format(
            self.normal, self.area, ', '.join([str(p.id) for p in self.polygons])
        )

    def __eq__(self, other):
        return self.polygons == other.polygons

    def __ne__(self, other):
        return not self == other

    def addPolygons(self, polygons):
        self.polygons |= polygons
        self.area = self.calculateArea()

    def calculateArea(self):
        return sum([p.area for p in self.polygons])

