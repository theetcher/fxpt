from . import com


class Vertex(object):
    """
    :type id: int
    :type point: maya.api.OpenMaya.MPoint
    :type normal: maya.api.OpenMaya.MVector
    :type normalId: int
    :type curvature: float
    :type absCurvature: float
    :type edges: set[fxpt.fx_smart_normal.edge.Edge]
    :type polygons: set[fxpt.fx_smart_normal.polygon.Polygon]
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
