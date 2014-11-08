class CtrlBase(object):

    def __init__(self, control, defaultValue):
        self.control = control
        self.controlName = self.getControlName()
        self.defaultValue = defaultValue
        self.prefData = {}

    def getControlName(self):
        raise NotImplementedError('Call to abstract method.')

    def ctrl2Data(self):
        self.setData()

    def data2Ctrl(self, prefData):
        self.setData(prefData)

    def getPrefData(self):
        return self.prefData

    def key(self, attr):
        return '{}_{}'.format(self.controlName, attr)

    def setData(self, prefData=None):
        if prefData is None:
            self.prefData = {}
        else:
            self.prefData = prefData

    def setAttr(self, attr, value):
        self.prefData[self.key(attr)] = value

    def getAttr(self, attr):
        key = self.key(attr)
        if key in self.prefData:
            return self.prefData[key]

