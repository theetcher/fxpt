class CtrlBase(object):

    def __init__(self, control, defaultValue):
        self.control = control
        self.defaultValue = defaultValue
        self.prefData = {}

    def ctrl2Data(self):
        raise NotImplementedError('Call to abstract method.')

    def data2Ctrl(self):
        raise NotImplementedError('Call to abstract method.')

    def setData(self, prefData=None):
        if prefData is None:
            self.prefData = {}
        else:
            self.prefData = prefData
