import sys
import os
import unittest
import subprocess


def run(testDir, rDir=None):
    if rDir:
        appendCoverageToSysPath()
        # noinspection PyUnresolvedReferences
        from fxpt.side_utils.coverage import coverage
        cov = coverage(config_file=testDir + '\\coverage.cfg')
        cov.start()

    testLoader = unittest.TestLoader()
    suite = testLoader.discover(testDir)
    unittest.TextTestRunner(verbosity=2).run(suite)

    if rDir:
        # noinspection PyUnboundLocalVariable
        cov.stop()
        cov.html_report(directory=rDir)


def runMaya(mayaExe, appDir, testDir, rDir=None):
    os.chdir(os.path.dirname(mayaExe))
    testDir = testDir.replace('\\', '/')
    if rDir:
        rDir = rDir.replace('\\', '/')
    cmd = [
        mayaExe,
        '-command',
        'python(\"from fxpt.fx_utils import testsRunner; testsRunner.run(\'{}\', \'{}\')\")'.format(testDir, rDir)
    ]
    env = os.environ.copy()
    env['MAYA_APP_DIR'] = appDir
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


def appendCoverageToSysPath():
    scriptDirSplitted = os.path.dirname(__file__).replace('\\', '/').split('/')
    coveragePath = '/'.join(scriptDirSplitted[:-1] + ['side_utils'])
    if not coveragePath in sys.path:
        sys.path.append(coveragePath)


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
