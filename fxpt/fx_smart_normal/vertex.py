from . import com


class Vertex(object):
    """
    :type id: int
    :type point: maya.api.OpenMaya.MPoint
    :type normal: maya.api.OpenMaya.MVector
    :type edges: list[fxpt.fx_smart_normal.edge.Edge]
    :type curvature: float
    """
    def __init__(self, vtxId):
        self.id = vtxId
        self.point = None
        self.normal = None
        self.curvature = None
        self.edges = []

    def __str__(self):
        return 'vertex({}): point={}, normal={}, curvature={}, edges=({})'.format(
            self.id, self.point, self.normal, self.curvature, ', '.join([str(e.id) for e in self.edges])
        )

    def calculateCurvature(self):
        self.curvature = com.ariMean([abs(e.curvature) for e in self.edges])
