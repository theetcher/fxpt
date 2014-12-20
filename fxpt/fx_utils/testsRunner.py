import sys
import os
import unittest


def run(testDir, rDir=None):
    if rDir:
        appendCoverageToSysPath()
        # noinspection PyUnresolvedReferences
        from fxpt.side_utils.coverage import coverage
        cov = coverage()
        cov.start()

    testLoader = unittest.TestLoader()
    suite = testLoader.discover(testDir)
    unittest.TextTestRunner().run(suite)

    if rDir:
        # noinspection PyUnboundLocalVariable
        cov.stop()
        cov.html_report(directory=rDir)


def usageAndExit():
    print '--- testsRunner Command Line Help ---'
    print 'testsRunner [-h|--help] -t|--testsDir testsDir [-r|--resultsDir resultsDir]'
    print '-h or --help        display this help'
    print '-t or --testsDir    root directory for tests search'
    print '-r or --resultsDir  code coverage results directory'
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
        opts, unusedParsedArgs = getopt.getopt(sys.argv[1:], 'ht:r:', ['help', 'testsDir=', 'resultsDir='])
    except getopt.GetoptError:
        usageAndExit()

    testsDir = resultsDir = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usageAndExit()
        elif opt in ('-t', '--testsDir'):
            testsDir = arg
        elif opt in ('-r', '--resultsDir'):
            resultsDir = arg

    if testsDir is None:
        usageAndExit()

    if not os.path.exists(testsDir):
        print 'Tests dir does not exists: {}'.format(testsDir)
        usageAndExit()

    if resultsDir is None:
        run(testsDir)
        sys.exit()

    if os.path.exists(resultsDir):
        run(testsDir, resultsDir)
        sys.exit()
    else:
        print 'Results dir does not exists: {}'.format(resultsDir)
        usageAndExit()