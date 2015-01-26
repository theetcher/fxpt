from fxpt.fx_utils.utils import pathToSlash

# style not finished
TOOLBAR_BUTTON_STYLE = """
QToolButton:checked{
    color: #000000;
    background-color: #5c5c5c;

    border-radius: 3px;
    border-style: dotted;
    border-color: black;
    border-width: 1px;

    margin-top:1px;
    margin-right:1px;
    margin-bottom:1px;
    margin-left:1px;

    padding:3px
}
"""

from fxpt.fx_utils.qtFontCreator import QtFontCreator
from fxpt.fx_utils.utils import getFxUtilsDir
qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getLetterSize('i')


def cleanupPath(path):
    return pathToSlash(path.strip()).rstrip('/')
