import os
from fxpt.fx_prefsaver import PrefSaver, Serializers
from com import REF_ROOT_VAR_NAME

ROOTS_CFG_OPT_VAR = 'fx_refSystem_roots'


# noinspection PyAttributeOutsideInit
class RootsCfgHandler(object):

    def __init__(self):
        self.roots = None

        self.initCfg()
        self.loadCfg()

    def initCfg(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(ROOTS_CFG_OPT_VAR))
        self.prefSaver.addVariable('roots', self.getterRoots, self.setterRoots, {'': True})

    def getterRoots(self):
        return self.roots

    def setterRoots(self, value):
        self.roots = value

    def loadCfg(self):
        self.prefSaver.loadPrefs()
        # TODO: if active roots number is wrong should defaults to first record or to empty cfg
        # TODO: try except if var is corrupted

    def saveCfg(self):
        self.prefSaver.savePrefs()
        self.setEnvVar()

    def setEnvVar(self):
        os.environ[REF_ROOT_VAR_NAME] = self.getCurrentRoot()

    def getCurrentRoot(self):
        self.loadCfg()
        for root, isActive in self.roots.items():
            if isActive:
                return root
        assert False, 'no active root in cfg.'

    def getRoots(self):
        self.loadCfg()
        return self.roots
