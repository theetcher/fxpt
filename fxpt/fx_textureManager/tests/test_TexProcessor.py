import unittest

from fxpt.fx_textureManager import TexProcessor


def patchName(name):
    return '{}.{}'.format(__name__, name)


class TexProcessorTests(unittest.TestCase):

    def test_TexProcessor_can_be_created(self):
        TexProcessor.TexProcessor()

    def test_TexProcessor_collectTexNodes(self):
        tp = TexProcessor.TexProcessor()
        tp.collectTexNodes()
