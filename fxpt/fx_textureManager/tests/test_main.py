import unittest
import types
from fxpt.side_utils.mock import patch  # pragma: no cover
from fxpt.fx_textureManager.tests import comTests

from fxpt.fx_textureManager import fx_textureManager


def patchName(name):
    return '{}.{}'.format(__name__, name)


class TexManagerTestMain(unittest.TestCase):

    def test_run_exists(self):
        self.assertTrue(hasattr(fx_textureManager, 'run'))

    def test_run_is_function(self):
        self.assertIs(type(fx_textureManager.run), types.FunctionType)

    @patch(patchName('fx_textureManager.run'))
    def test_mock(self, mock_func):
        mock_func.return_value = True
        self.assertTrue(mock_func())

    @comTests.skipInNoUIMode()
    def test_only_in_ui_mode(self):
        self.assertTrue(comTests.getUIAvailable())



