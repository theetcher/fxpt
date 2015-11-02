import os
import unittest
import maya.cmds as m
from maya.mel import eval as meval

from fxpt.fx_utils.utils import getFxptLocation

from fxpt.fx_textureManager import tex_node
from com_tests import loadMayaScene


def patchName(name):
    return '{}.{}'.format(__name__, name)


def setFileNodeWithAbsPath():
    m.setAttr('fileNodeWithAbsPath.ftn', getFxptLocation() + '/fxpt/fx_textureManager/icons/filter_active.png', typ='string')


def setupScene():
    meval('setProject "{}/fxpt/fx_textureManager/tests/testMayaProject"'.format(getFxptLocation()))
    loadMayaScene(getFxptLocation() + '/fxpt/fx_textureManager/tests/testMayaProject/scenes/testScene_01.mb')
    setFileNodeWithAbsPath()
    os.environ['FXPT_LOCATION'] = getFxptLocation()


# def createTexNodes():
#     return [TexNode.TexNode(node, attr) for node, attr in [
#             ('fileNodeWithProjPath', 'ftn'),
#             ('fileNodeWithAbsPath', 'ftn'),
#             ('fileNodeWithEnvVar', 'ftn'),
#             ('fileNodeWithNetworkPath', 'ftn'),
#             ('fileNodeWithInvalidPath', 'ftn'),
#             ]]


class TexNodeTests(unittest.TestCase):

    def test_TexNode_can_be_created(self):
        tex_node.TexNode('testNode', 'testAttr')

    def test_TexNode_node_and_attr_setters_getters(self):
        tn = tex_node.TexNode('testNode', 'testAttr')
        self.assertEqual(tn.node, 'testNode')
        self.assertEqual(tn.attr, 'testAttr')
        self.assertEqual(tn.getNode(), 'testNode')
        self.assertEqual(tn.getAttr(), 'testAttr')

    def test_TexNode_getFullAttrName(self):
        tn = tex_node.TexNode('someNode', 'someAttr')
        self.assertEqual(tn.getFullAttrName(), '{}.{}'.format('someNode', 'someAttr'))

    def test_TexNode_getAttrValue(self):
        setupScene()

        nodesAttrsValues = [
            ('fileNodeWithProjPath', 'ftn', getFxptLocation() + '/fxpt/fx_textureManager/tests/testMayaProject/sourceimages/testTex_exit.png'),
            ('fileNodeWithAbsPath', 'ftn', getFxptLocation() + '/fxpt/fx_textureManager/icons/filter_active.png'),
            ('fileNodeWithEnvVar', 'ftn', '%FXPT_LOCATION%/fxpt/fx_textureManager/icons/copy.png'),
            ('fileNodeWithInvalidEnvVar', 'ftn', '%INVALID_ENV_VAR%/fxpt/fx_textureManager/icons/copy.png'),
            ('fileNodeWithNetworkPath', 'ftn', '//BLACK/C$/GitHub/fxpt/fxpt/fx_textureManager/icons/retarget.png'),
            ('fileNodeWithInvalidPath', 'ftn', 'some/path/tex.png'),
            ('someNodeWithTextures1', 'texture', '%FXPT_LOCATION%/fxpt/fx_textureManager/icons/copy.png'),
            ('someNodeWithTextures1', 'texture1', 'sourceimages/testTex_exit.png'),
            ('someNodeWithTextures1', 'texture2', '//BLACK/C$/GitHub/fxpt/fxpt/fx_textureManager/icons/retarget.png'),
            ('someNodeWithTextures2', 'texture', '%FXPT_LOCATION%/fxpt/fx_textureManager/icons/copy.png'),
            ('someNodeWithTextures2', 'texture1', 'sourceimages/testTex_exit.png'),
            ('someNodeWithTextures2', 'texture2', '')
        ]

        for node, attr, value in nodesAttrsValues:
            tn = tex_node.TexNode(node, attr)
            self.assertEqual(tn.getAttrValue(), value)

    def test_TexNode_fileExists(self):
        setupScene()

        nodesAttrsValues = [
            ('fileNodeWithProjPath', 'ftn', True),
            ('fileNodeWithAbsPath', 'ftn', True),
            ('fileNodeWithEnvVar', 'ftn', True),
            ('fileNodeWithInvalidEnvVar', 'ftn', False),
            ('fileNodeWithNetworkPath', 'ftn', True),
            ('fileNodeWithInvalidPath', 'ftn', False),
            ('someNodeWithTextures1', 'texture', True),
            ('someNodeWithTextures1', 'texture1', False),
            ('someNodeWithTextures1', 'texture2', True),
            ('someNodeWithTextures2', 'texture', True),
            ('someNodeWithTextures2', 'texture1', False),
            ('someNodeWithTextures2', 'texture2', False)
        ]

        for node, attr, value in nodesAttrsValues:
            tn = tex_node.TexNode(node, attr)
            self.assertEqual(tn.fileExists(), value)
