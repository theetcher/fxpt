import unittest

from fxpt.fx_textureManager import TexProcessor
from fxpt.fx_textureManager import TexNode


def patchName(name):
    return '{}.{}'.format(__name__, name)


class TexProcessorTests(unittest.TestCase):

    def test_TexProcessor_can_be_created(self):
        TexProcessor.TexProcessor()

    def test_TexProcessor_collectTexNodes(self):
        tp = TexProcessor.TexProcessor()
        tp.collectTexNodes()
        self.assertEqual(len(tp.texNodes), 12)

        attrNames = [
            'fileNodeWithProjPath.fileTextureName',
            'fileNodeWithAbsPath.fileTextureName',
            'fileNodeWithEnvVar.fileTextureName',
            'fileNodeWithInvalidEnvVar.fileTextureName',
            'fileNodeWithNetworkPath.fileTextureName',
            'fileNodeWithInvalidPath.fileTextureName',
            '|someNodeWithTextures1.texture',
            '|someNodeWithTextures1.texture1',
            '|someNodeWithTextures1.texture2',
            '|someNodeWithTextures2.texture',
            '|someNodeWithTextures2.texture1',
            '|someNodeWithTextures2.texture2'
        ]

        for tn in tp.texNodes:
            self.assertIn(tn.getFullAttrName(), attrNames)

    def test_TexProcessor_getTexNodes(self):
        tp = TexProcessor.TexProcessor()
        tp.texNodes.append(TexNode.TexNode('node', 'attr'))
        result = tp.getTexNodes()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TexNode.TexNode)