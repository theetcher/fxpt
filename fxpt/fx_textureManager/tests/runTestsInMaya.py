import os
from fxpt.fx_utils import testsRunner


def run():
    testsRunner.run(
        os.path.dirname(__file__),
        os.path.dirname(__file__) + '/htmlcov'
    )
