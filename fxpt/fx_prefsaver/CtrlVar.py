class CtrlVar(object):

    def __init__(self, name, getter, setter, defaultValue):
        self.name = name
        self.getter = getter
        self.setter = setter
        self.defaultValue = defaultValue

        self.prefData = None

    def getControlName(self):
        return self.name

    def getPrefData(self):
        return self.prefData

    def ctrl2Data(self):
        self.prefData = self.getter()

    def data2Ctrl(self, prefDataGlobal):
        self.setData(prefDataGlobal)
        self.setter(self.prefData)

    def setData(self, prefDataGlobal=None):
        if (prefDataGlobal is None) or (self.getControlName() not in prefDataGlobal):
            self.prefData = self.defaultValue
        else:
            self.prefData = prefDataGlobal[self.getControlName()]