class Edge(object):
    """
    :type id: int
    :type v1: fxpt.fx_smart_normal.vertex.Vertex
    :type v2: fxpt.fx_smart_normal.vertex.Vertex
    :type curvature: float
    """
    def __init__(self, edgeId, v1, v2):
        self.id = edgeId
        self.v1 = v1
        self.v2 = v2
        self.curvature = None
        self.calculateCurvature()

    def __str__(self):
        return 'edge({}): v1={}, v2={}, curvature={}'.format(self.id, self.v1.id, self.v2.id, self.curvature)

    def calculateCurvature(self):
        normDiff = self.v2.normal - self.v1.normal
        pointDiff = self.v2.point - self.v1.point
        self.curvature = (normDiff * pointDiff) / (pointDiff * pointDiff)
