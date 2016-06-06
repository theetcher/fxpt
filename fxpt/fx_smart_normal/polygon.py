class Polygon(object):
    """
    :type id: int
    :type normal: maya.api.OpenMaya.MVector
    :type area: float
    :type vertices: set[fxpt.fx_smart_normal.vertex.Vertex]
    :type edges: set[fxpt.fx_smart_normal.edge.Edge]
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
