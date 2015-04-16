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


def makeWritable(path):
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)


def isWritable(path):
    if os.path.exists(path):
        return os.access(path.lower().strip(), os.W_OK)
    return True
