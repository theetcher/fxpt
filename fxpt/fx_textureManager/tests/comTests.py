import unittest

_uiAvailable = False


def setUIAvailable():
    global _uiAvailable
    _uiAvailable = True


def getUIAvailable():
    return _uiAvailable


def skipInNoUIMode():
    return unittest.skipUnless(getUIAvailable(), 'Skipped in no UI mode.')