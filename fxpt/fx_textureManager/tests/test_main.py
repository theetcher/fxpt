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

    def test_run_is_a_function(self):
        self.assertIs(
            type(fx_textureManager.run),
            types.FunctionType,
        )

    @skipInBatchMode()
    def test_run(self):
        self.assertIsNone(fx_textureManager.mainWin, 'There should be no window on test start')
        fx_textureManager.run()
        self.assertIsInstance(
            fx_textureManager.mainWin,
            QtGui.QMainWindow
        )

    @skipInBatchMode()
    def test_getMayaMainWindowPtr_returns_something(self):
        self.assertTrue(fx_textureManager.getMayaMainWindowPtr())

    @patch(patchName('fx_textureManager.apiUI.MQtUtil.mainWindow'))
    def test_getMayaMainWindowPtr_raises_exception(self, mockGetPtr):
        mockGetPtr.return_value = None
        self.assertRaises(RuntimeError, fx_textureManager.getMayaMainWindowPtr)

    @skipInBatchMode()
    def test_getMayaQMainWindow_returns_QMainWindow(self):
        ptr = fx_textureManager.getMayaMainWindowPtr()
        self.assertIs(
            type(fx_textureManager.getMayaQMainWindow(ptr)),
            QtGui.QMainWindow
        )