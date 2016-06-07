from . import geom_processor


class Normalizer(object):
    def __init__(self, meshTransform):
        # self.meshTransform = meshTransform
        self.geomProcessor = geom_processor.GeomProcessor(meshTransform)

    def process(self, params):
        self.geomProcessor.params = params
        self.geomProcessor.process()

    def updateDisplay(self, params):
        self.geomProcessor.params = params
        self.geomProcessor.display()

