import os
from fxpt.fx_utils import tests_runner


def run():
    tests_runner.run(
        os.path.dirname(__file__),
        os.path.dirname(__file__) + '/htmlcov'
    )
