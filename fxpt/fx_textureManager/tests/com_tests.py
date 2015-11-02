import unittest
import maya.cmds as m

from fxpt.fx_utils.utils import getFxptLocation


def getTestEnvVar():
    return 'FXPT_LOCATION', getFxptLocation()


def isMayaInBatchMode():
    return bool(m.about(batch=True))


def skipInBatchMode():
    return unittest.skipIf(isMayaInBatchMode(), 'Skipped in batch mode.')


def loadMayaScene(scene):
    return m.file(scene, open=True, force=True, options='v=0;', typ='mayaBinary')
