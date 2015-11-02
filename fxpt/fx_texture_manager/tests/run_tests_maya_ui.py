import os
from fxpt.fx_utils import tests_runner


def run():
    tests_runner.runMaya(
        'C:/Program Files/Autodesk/Maya2014/bin/maya.exe',
        'C:/FXTools/FX',
        os.path.dirname(__file__),
        os.path.dirname(__file__) + '/htmlcov'
    )


if __name__ == '__main__':
    run()