from fxpt.fx_prefsaver import prefsaver, serializers

OPT_VAR_NAME_COMMON_PREFS = 'fx_refsystem_global_prefs'


class GlobalPrefsHandler(object):

    KEY_LAST_BROWSED_CREATE_REF = 'lastBrowsedCreateRef'
    KEY_LAST_BROWSED_DIR = 'lastBrowsedDir'
    KEY_LAST_BROWSED_SOURCE = 'lastBrowsedSource'

    def __init__(self):
        self.globalPrefs = None
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME_COMMON_PREFS))
        self.initPrefs()

    def initPrefs(self):
        self.prefSaver.addVariable('globalPrefs', self.getterGlobalPrefs, self.setterGlobalPrefs, dict())

    def savePrefs(self):
        self.prefSaver.savePrefs()

    def loadPrefs(self):
        self.prefSaver.loadPrefs()

    def setterGlobalPrefs(self, value):
        self.globalPrefs = value

    def getterGlobalPrefs(self):
        return self.globalPrefs

    def getValue(self, key):
        return self.globalPrefs.get(key, None)

    def setValue(self, key, value):
        self.globalPrefs[key] = value

