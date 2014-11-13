class CtrlBase(object):

    def __init__(self, control, defaultValue):
        self.control = control
        self.controlName = self.retrieveControlName()
        self.defaultValue = defaultValue
        self.prefData = {}

    def retrieveControlName(self):
        raise NotImplementedError('Call to abstract method.')

    def getControlName(self):
        return self.controlName

    def ctrl2Data(self):
        self.setData()

    def data2Ctrl(self, prefDataGlobal):
        self.setData(prefDataGlobal)

    def getPrefData(self):
        return self.prefData

    def setData(self, prefDataGlobal=None):
        if (prefDataGlobal is None) or (self.getControlName() not in prefDataGlobal):
            self.prefData = {}
        else:
            self.prefData = prefDataGlobal[self.getControlName()]

    def setAttr(self, attr, value):
        self.prefData[attr] = value

    def getAttr(self, attr, noDefault=False):
        if attr in self.prefData:
            return self.prefData[attr]
        else:
            if noDefault:
                return None
            else:
                return self.defaultValue

