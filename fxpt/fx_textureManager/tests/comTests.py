import unittest
import maya.cmds as m


def isMayaInBatchMode():
    return bool(m.about(batch=True))


def skipInBatchMode():
    return unittest.skipIf(isMayaInBatchMode(), 'Skipped in batch mode.')