from math import pi


class Edge(object):
    """
    :type id: int
    :type v1: fxpt.fx_smart_normal.vertex.Vertex
    :type v2: fxpt.fx_smart_normal.vertex.Vertex
    :type polygons: set[fxpt.fx_smart_normal.polygon.Polygon]
    :type curvature: float
    :type edgeAngle: float
    """
    def __init__(self, edgeId, v1, v2):
        self.id = edgeId
        self.v1 = v1
        self.v2 = v2
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
        if len(self.polygons) == 2:
            polygonList = list(self.polygons)
            self.edgeAngle = polygonList[0].normal.angle(polygonList[1].normal) * 180 / pi

