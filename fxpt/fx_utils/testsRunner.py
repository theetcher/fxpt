import sys
import os
import unittest
import subprocess


def appendCoverageToSysPath():
    scriptDirSplitted = os.path.dirname(__file__).replace('\\', '/').split('/')
    coveragePath = '/'.join(scriptDirSplitted[:-1] + ['side_utils'])
    if not coveragePath in sys.path:
        sys.path.append(coveragePath)

appendCoverageToSysPath()
from fxpt.side_utils import coverage


class CoverageCtx():
    def __init__(self, testDir, rDir):
        self.testDir = testDir
        self.rDir = rDir

    def __enter__(self):
        if self.rDir:
            # noinspection PyUnresolvedReferences
            self.cov = coverage.coverage(config_file=self.getCoverageCfg(self.testDir))
            self.cov.start()

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.rDir:
            self.cov.stop()
            self.cov.html_report(directory=self.rDir)

    # noinspection PyMethodMayBeStatic
    def getCoverageCfg(self, testDir):
        coverageCfgName = 'coverage.cfg'
        specificCfg = '{}/{}'.format(testDir, coverageCfgName)
        globalCfg = '{}/{}'.format(os.path.dirname(coverage.__file__), coverageCfgName)

        if os.path.exists(specificCfg):
            return specificCfg
        else:
            return globalCfg


def getFxptRoot():
    scriptDir = os.path.dirname(__file__).replace('\\', '/')
    return '/'.join(scriptDir.split('/')[:-2])


def run(testDir, rDir=None):
    with CoverageCtx(testDir, rDir):
        testLoader = unittest.TestLoader()
        suite = testLoader.discover(testDir)
        unittest.TextTestRunner(verbosity=2).run(suite)


def runMaya(mayaExe, appDir, testDir, rDir=None):
    os.chdir(os.path.dirname(mayaExe))
    testDir = testDir.replace('\\', '/')
    if rDir:
        rDir = rDir.replace('\\', '/')
    cmd = [
        mayaExe,
        '-command',
        'python(\"from fxpt.fx_utils import testsRunner; testsRunner.run(\'{0}\', \'{1}\')\")'.format(testDir, rDir)
    ]

    env = os.environ.copy()
    env['MAYA_APP_DIR'] = appDir
    # if i will not set up PYTHONPATH to fxpt root
    # it will be a problem with running tests in Maya in UI mode with Qt stuff FROM PYCHARM.
    #TODO: find out which path actually is a problem.
    env['PYTHONPATH'] = getFxptRoot()

    process = subprocess.Popen(cmd, stderr=subprocess.STDOUT, env=env)
    process.wait()


def usageAndExit():
    print '--- testsRunner Command Line Help ---'
    print 'testsRunner [-h|--help] -t|--testsDir testsDir [-r|--resultsDir resultsDir] [-m|--mayaBatchExe mayaBatchExe -a|--mayaAppDir mayaAppDir]'
    print '-h or --help          display this help'
    print '-t or --testsDir      root directory for tests search'
    print '-r or --resultsDir    code coverage results directory'
    print '-m or --mayaBatchExe  mayabatch.exe path'
    print '-a or --mayaAppDir    MAYA_APP_DIR path'
    sys.exit()


if __name__ == '__main__':
    import getopt

    opts = None
    try:
        opts, unusedParsedArgs = getopt.getopt(sys.argv[1:], 'ht:r:m:a:', ['help', 'testsDir=', 'resultsDir=', 'mayaBatchExe=', 'mayaAppDir='])
    except getopt.GetoptError:
        usageAndExit()

    testsDir = resultsDir = mayaBatchExe = mayaAppDir = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usageAndExit()
        elif opt in ('-t', '--testsDir'):
            testsDir = arg
        elif opt in ('-r', '--resultsDir'):
            resultsDir = arg
        elif opt in ('-m', '--mayaBatchExe'):
            mayaBatchExe = arg
        elif opt in ('-a', '--mayaAppDir'):
            mayaAppDir = arg

    if testsDir is None:
        usageAndExit()

    if not os.path.exists(testsDir):
        print 'Tests dir does not exists: {}'.format(testsDir)
        usageAndExit()

    if (resultsDir is not None) and (not os.path.exists(resultsDir)):
        print 'Results dir does not exists: {}'.format(resultsDir)
        usageAndExit()

    if mayaBatchExe is None:
        run(testsDir, resultsDir)
        sys.exit()

    if (mayaBatchExe is not None) and (not os.path.exists(mayaBatchExe)):
        print 'Cannot find mayabatch.exe: {}'.format(mayaBatchExe)
        usageAndExit()

    if mayaAppDir is None:
        print 'Provide MAYA_APP_DIR path.'
        usageAndExit()

    if (mayaAppDir is not None) and (not os.path.exists(mayaAppDir)):
        print 'MAYA_APP_DIR does not exists: {}'.format(mayaAppDir)
        usageAndExit()

    runMaya(mayaBatchExe, mayaAppDir, testsDir, resultsDir)
