import unittest
from fxpt.side_utils.mock import patch

from fxpt.fx_textureManager import fx_textureManager


def setUpModule():
    print 'setUpModule() exec!!!'
    print __name__


class TexManagerTestMain(unittest.TestCase):

    def test_run(self):
        fx_textureManager.run()

    @patch(__name__ + '.fx_textureManager.someFunc')
    # @patch('test_main.fx_textureManager.someFunc')
    # @patch('fxpt.fx_textureManager.fx_textureManager.someFunc')
    def test_mock(self, mock_func):
        fx_textureManager.someFunc()

        mock_func.return_value = 0
        self.assertTrue(mock_func())




