import unittest
import maya.cmds as m

from fxpt.fx_utils.utils import getFxptLocation

from fxpt.fx_textureManager import TexNode
from comTests import loadMayaScene


def patchName(name):
    return '{}.{}'.format(__name__, name)


def setFileNodeWithAbsPath():
    m.setAttr('fileNodeWithAbsPath.ftn', getFxptLocation() + '/fxpt/fx_textureManager/icons/filterActive.png', typ='string')


class TexNodeTests(unittest.TestCase):

    def test_TexNode_can_be_created(self):
        TexNode.TexNode('testNode', 'testAttr')

    def test_TexNode_node_and_attr_setters_getters(self):
        tn = TexNode.TexNode('testNode', 'testAttr')
        self.assertEqual(tn.node, 'testNode')
        self.assertEqual(tn.attr, 'testAttr')
        self.assertEqual(tn.getNode(), 'testNode')
        self.assertEqual(tn.getAttr(), 'testAttr')

    def test_TexNode_getFullAttrName(self):
        tn = TexNode.TexNode('someNode', 'someAttr')
        self.assertEqual(tn.getFullAttrName(), '{}.{}'.format('someNode', 'someAttr'))

    def test_TexNode_getAttrValue(self):
        #TODO: update this test when attribute other than "ftn" appear
        loadMayaScene(getFxptLocation() + '/fxpt/fx_textureManager/tests/testMayaProject/scenes/testScene_01.mb')
        setFileNodeWithAbsPath()

        nodesAttrsValues = [
            ('fileNodeWithProjPath', 'ftn', getFxptLocation() + '/fxpt/fx_textureManager/tests/testMayaProject/sourceimages/testTex_exit.png'),
            ('fileNodeWithAbsPath', 'ftn', getFxptLocation() + '/fxpt/fx_textureManager/icons/filterActive.png'),
            ('fileNodeWithEnvVar', 'ftn', '%FXPT_LOCATION%/fxpt/fx_textureManager/icons/copy.png'),
            ('fileNodeWithNetworkPath', 'ftn', '//BLACK/C$/GitHub/fxpt/fxpt/fx_textureManager/icons/retarget.png'),
            ('fileNodeWithInvalidPath', 'ftn', 'some/path/tex.png')
        ]

        for node, attr, value in nodesAttrsValues:
            tn = TexNode.TexNode(node, attr)
            self.assertEqual(tn.getAttrValue(), value)