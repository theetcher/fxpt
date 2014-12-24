import os
from fxpt.fx_utils import testsRunner
from fxpt.fx_textureManager.tests import comTests


def runStandalone():
    testsRunner.runMaya(
        'C:/Program Files/Autodesk/Maya2014/bin/mayabatch.exe',
        'C:/FXTools/FX',
        os.path.dirname(__file__),
        os.path.dirname(__file__) + '/htmlcov'
    )


def runInMaya():
    comTests.setUIAvailable()
    testsRunner.run(
        os.path.dirname(__file__),
        os.path.dirname(__file__) + '/htmlcov'
    )


if __name__ == '__main__':
    runStandalone()