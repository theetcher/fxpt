# class ProcTypes(object):
#
#     ProcPaste = 1

import re


class ProcessorPaste(object):

    def __init__(self, tns, newFilename):
        self.tns = tns
        self.newFilename = newFilename

    def execute(self):
        for tn in self.tns:
            tn.setAttrValue(self.newFilename)


class ProcessorSearchReplace(object):

    def __init__(self, tns, oldStr, newStr, caseSensitive):
        self.tns = tns
        self.oldStr = oldStr
        self.newStr = newStr
        self.caseSensitive = caseSensitive

    def execute(self):
        if not self.oldStr:
            return

        if self.caseSensitive:
            pattern = re.compile(re.escape(self.oldStr), re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(self.oldStr))

        for tn in self.tns:
            oldValue = tn.getAttrValue()
            newValue = pattern.sub(self.newStr, oldValue)
            if newValue != oldValue:
                tn.setAttrValue(newValue)
