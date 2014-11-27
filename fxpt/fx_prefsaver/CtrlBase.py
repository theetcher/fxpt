#TODO!: CtrlVar is base?


class CtrlBase(object):

    def __init__(self, control, defaultValue):
        self.control = control
        self.controlName = self.retrieveControlName()
        self.defaultValue = defaultValue
        self.prefData = {}

        self.attr = None
        self.ctrlGetter = None
        self.ctrlSetter = None

    def setupGetSetVars(self, attr, getter, setter):
        self.attr = attr
        self.ctrlGetter = getter
        self.ctrlSetter = setter

    def retrieveControlName(self):
        raise NotImplementedError('Call to abstract method.')

    def getControlName(self):
        return self.controlName

    def ctrl2Data(self):
        self.setData()
        self.ctrl2DataProcedure()

    def ctrl2DataProcedure(self):
        self.setAttr(self.attr, self.ctrlGetter())

    def data2Ctrl(self, prefDataGlobal):
        self.setData(prefDataGlobal)
        self.data2CtrlProcedure()

    def data2CtrlProcedure(self):
        self.ctrlSetter(self.getAttr(self.attr))

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


