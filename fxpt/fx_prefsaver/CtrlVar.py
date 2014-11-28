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

    def data2Ctrl(self, value):
        self.setData(value)
        self.setter(self.prefData)

    def setData(self, prefData=None):
        self.prefData = prefData if prefData else self.defaultValue
