import unittest
import types
from PySide import QtGui
from fxpt.side_utils.mock import patch
from fxpt.fx_textureManager.tests.comTests import skipInBatchMode

from fxpt.fx_textureManager import fx_textureManager


def patchName(name):
    return '{}.{}'.format(__name__, name)


class TexManagerTestMain(unittest.TestCase):

    def test_run_exists(self):
        self.assertTrue(hasattr(fx_textureManager, 'run'), 'fx_textureManager.run() exists')

    def test_run_is_function(self):
        self.assertIs(
            type(fx_textureManager.run),
            types.FunctionType,
        )

    @skipInBatchMode()
    def test_getMayaMainWindowPtr_returns_something(self):
        self.assertTrue(fx_textureManager.getMayaMainWindowPtr())

    @skipInBatchMode()
    def test_getMayaQMainWindow_returns_QMainWindow(self):
        ptr = fx_textureManager.getMayaMainWindowPtr()
        self.assertIs(
            type(fx_textureManager.getMayaQMainWindow(ptr)),
            QtGui.QMainWindow
        )

    @patch(patchName('fx_textureManager.run'))
    def test_mock(self, mock_func):
        mock_func.return_value = True
        self.assertTrue(fx_textureManager.run())


