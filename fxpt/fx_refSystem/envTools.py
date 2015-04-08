import os

REF_ROOT_NAME = 'REF_ROOT'
SOURCE_DIR = 'source'


def getRefRootVarName():
    return REF_ROOT_NAME


def getRefRootVarNamePercent():
    return '%{}%'.format(getRefRootVarName())


def getRefRoot():
    refRootEnvVar = getRefRootVarName()
    if refRootEnvVar in os.environ:
        return os.environ[refRootEnvVar].replace('\\', '/')
    return ''


def getSourceDir():
    return os.path.join(getRefRoot(), SOURCE_DIR)