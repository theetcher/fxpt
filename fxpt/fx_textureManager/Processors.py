# class ProcTypes(object):
#
#     ProcPaste = 1


class ProcessorPaste(object):

    def __init__(self, tns, newFilename):
        self.tns = tns
        self.newFilename = newFilename

    def execute(self):
        for tn in self.tns:
            tn.setAttrValue(self.newFilename)


class ProcessorSearchReplace(object):

    def __init__(self, tns, oldStr, newStr):
        self.tns = tns
        self.oldStr = oldStr
        self.newStr = newStr

    def execute(self):
        for tn in self.tns:
            oldValue = tn.getAttrValue()
            newValue = oldValue.replace(self.oldStr, self.newStr)
            if newValue != oldValue:
                tn.setAttrValue(newValue)
