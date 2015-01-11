# class ProcTypes(object):
#
#     ProcPaste = 1

import os
import re

from fxpt.fx_textureManager.com import cleanupPath
#from fxpt.fx_utils.watch import watch


class ProcessorBase(object):

    def __init__(self):
        self.logString = []

    def log(self, text):
        self.logString.append(text)

    def printLog(self):
        for s in self.logString:
            print s

    def execute(self):
        raise NotImplementedError('Call to abstract method.')


class ProcessorPaste(ProcessorBase):

    def __init__(self, tns, newFilename):
        super(ProcessorPaste, self).__init__()
        self.tns = tns
        self.newFilename = newFilename

    def execute(self):
        for tn in self.tns:
            tn.setAttrValue(self.newFilename)


class ProcessorSearchReplace(ProcessorBase):

    def __init__(self, tns, oldStr, newStr, caseSensitive):
        super(ProcessorSearchReplace, self).__init__()
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


class ProcessorRetarget(ProcessorBase):

    def __init__(self, tns, retargetRoot, forceRetarget):
        super(ProcessorRetarget, self).__init__()
        self.tns = tns
        self.retargetRoot = retargetRoot
        self.forceRetarget = forceRetarget

    def execute(self):
        texDb = self.getTexDb()
        for tn in self.tns:
            texName = os.path.basename(tn.getAttrValue())
            texNameLower = texName.lower()
            if texNameLower in texDb:
                tn.setAttrValue(texDb[texNameLower])
            else:
                if self.forceRetarget:
                    tn.setAttrValue('{}/{}'.format(self.retargetRoot, texName))
                    self.log('ProcessorRetarget: "{}" was not found in target directory -> Retargeting to root dir.'.format(texName))
        self.printLog()

    def getTexDb(self):
        texDb = {}
        for root, directories, files in os.walk(self.retargetRoot):
            for f in files:
                fullPath = cleanupPath(os.path.join(root, f))
                lowCaseFilename = f.lower()
                if lowCaseFilename in texDb:
                    self.log('ProcessorRetarget: duplicate texture in retarget directory: ' + fullPath + ' -> Skipped.')
                else:
                    texDb[lowCaseFilename] = fullPath
        return texDb

