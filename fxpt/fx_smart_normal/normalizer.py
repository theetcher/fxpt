from . import geom_processor


class Normalizer(object):
    def __init__(self, meshTransform):
        self.meshTransform = meshTransform
        self.geomProcessor = geom_processor.GeomProcessor(meshTransform)

