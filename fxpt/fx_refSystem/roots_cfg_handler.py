import os
from fxpt.fx_prefsaver import prefsaver, serializers
from com import REF_ROOT_VAR_NAME

ROOTS_CFG_OPT_VAR = 'fx_refSystem_roots'

ROOTS_DEFAULT_VALUE = {'': True}


# noinspection PyAttributeOutsideInit
class RootsCfgHandler(object):

    def __init__(self):
        self.roots = None

        self.initCfg()
        self.loadCfg()

    def initCfg(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(ROOTS_CFG_OPT_VAR))
        # self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerFileJson(os.path.dirname(__file__) + '/test.cfg'))
        self.prefSaver.addVariable('roots', self.getterRoots, self.setterRoots, self.getDefaultRootsValue())

    def getterRoots(self):
        return self.roots

    def setterRoots(self, value):
        self.roots = value

    # noinspection PyMethodMayBeStatic
    def getDefaultRootsValue(self):
        return dict(ROOTS_DEFAULT_VALUE)

    def loadCfg(self):
        # noinspection PyBroadException
        try:
            self.prefSaver.loadPrefs()
        except Exception:
            self.roots = self.getDefaultRootsValue()
            return

        self.cleanupRootsDict()

    def cleanupRootsDict(self):
        if len(self.roots) < 1:
            self.roots = self.getDefaultRootsValue()
            return

        if '' not in self.roots:
            self.roots = self.getDefaultRootsValue()
            return

        activeCount = len([v for v in self.roots.values() if v])

        if activeCount == 1:
            return
        elif activeCount < 1:
            self.roots[''] = True
            return
        else:
            for root in self.roots:
                if root == '':
                    self.roots[root] = True
                else:
                    self.roots[root] = False

    def saveCfg(self):
        self.cleanupRootsDict()
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
