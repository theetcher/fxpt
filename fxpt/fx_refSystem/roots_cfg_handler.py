from fxpt.fx_prefsaver import PrefSaver, Serializers


ROOTS_CFG_OPT_VAR = 'fx_refSystem_roots'


# noinspection PyAttributeOutsideInit
class RootsCfgHandler(object):

    def __init__(self):
        self.currentRoot = None
        self.roots = None

        self.initCfg()
        self.loadCfg()

    def initCfg(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(ROOTS_CFG_OPT_VAR))
        self.prefSaver.addVariable('currentRoot', self.getterCurrentRoot, self.setterCurrentRoot, 0)
        self.prefSaver.addVariable('roots', self.getterRoots, self.setterRoots, [''])

    def getterCurrentRoot(self):
        return self.currentRoot

    def setterCurrentRoot(self, value):
        self.currentRoot = value

    def getterRoots(self):
        return self.roots

    def setterRoots(self, value):
        self.roots = value

    def loadCfg(self):
        self.prefSaver.loadPrefs()

    def saveCfg(self):
        self.prefSaver.savePrefs()

    def getCurrentRootIndex(self):
        self.loadCfg()
        return self.currentRoot

    def getCurrentRoot(self):
        self.loadCfg()
        return self.roots[self.getCurrentRootIndex()]

    def getRoots(self):
        self.loadCfg()
        return self.roots
