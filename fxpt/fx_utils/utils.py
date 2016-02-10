import os
import stat


def cleanupPath(path):
    return pathToSlash(path).strip()


def pathToSlash(path):
    return path.replace('\\', '/')


def pathToBackslash(path):
    return path.replace('/', '\\')


def getFxptLocation():
    scriptDir = pathToSlash(os.path.dirname(__file__))
    return '/'.join(scriptDir.split('/')[:-2])


def getFxUtilsDir():
    return pathToSlash(os.path.dirname(__file__))


def getUserCfgDir():
    origFxptCfgDir = pathToSlash('{}/Damage Inc/fxpt'.format(os.environ['APPDATA']))
    overrideFilename = '{}/.path_override'.format(origFxptCfgDir)
    if os.path.exists(overrideFilename):
        with open(overrideFilename, 'r') as f:
            overridePath = pathToSlash(f.readline().strip())
        return overridePath[:-1] if overridePath.endswith('/') else overridePath
    else:
        return origFxptCfgDir


def makeWritable(path):
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)


def isWritable(path):
    if os.path.exists(path):
        return os.access(path.lower().strip(), os.W_OK)
    return True

