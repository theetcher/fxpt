import os
from fxpt.fx_utils import testsRunner

testsRunner.runMaya(
    'C:/Program Files/Autodesk/Maya2014/bin/mayabatch.exe',
    'C:/FXTools/FX',
    os.path.dirname(__file__),
    os.path.dirname(__file__) + '/htmlcov'
)
