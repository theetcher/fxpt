import os
import re
import shutil

from fxpt.fx_utils.utils import makeWritable
from fxpt.fx_textureManager.com import cleanupPath
#from fxpt.fx_utils.watch import watch


class ProcessorBase(object):

    def __init__(self):
        self.logStrings = []

    def log(self, text):
        self.logStrings.append(text)

    def getLog(self):
        return self.logStrings

    def printLog(self):
        for s in self.logStrings:
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

    def __init__(self, tns, retargetRoot, forceRetarget, useSourceRoot, sourceRoot):
        super(ProcessorRetarget, self).__init__()
        self.tns = tns
        self.retargetRoot = retargetRoot
        self.forceRetarget = forceRetarget
        self.useSourceRoot = useSourceRoot
        self.sourceRoot = sourceRoot

    def execute(self):
        texDb = self.getTexDb()
        for tn in self.tns:

            tnAttrValue = tn.getAttrValue()

            # first try to find texture using source root
            if self.useSourceRoot:
                srcRootLower = self.sourceRoot.lower() + '/'
                if tnAttrValue.lower().startswith(srcRootLower):
                    probableNewValue = '{0}/{1}'.format(self.retargetRoot, tnAttrValue[len(srcRootLower):])
                    if os.path.exists(probableNewValue):
                        tn.setAttrValue(probableNewValue)
                        continue

            # if not found using source root, proceed with standard procedure
            texName = os.path.basename(tnAttrValue)
            texNameLower = texName.lower()
            if texNameLower in texDb:
                tn.setAttrValue(texDb[texNameLower])
            else:
                if self.forceRetarget:
                    tn.setAttrValue('{}/{}'.format(self.retargetRoot, texName))
                    self.log('ProcessorRetarget: "{0}" was not found in target directory -> Retargeting to root dir.'.format(texName))

    def getTexDb(self):
        texDb = {}
        for root, directories, files in os.walk(self.retargetRoot):
            for f in files:
                fullPath = cleanupPath(os.path.join(root, f))
                lowCaseFilename = f.lower()
                if lowCaseFilename in texDb:
                    self.log('ProcessorRetarget: duplicate texture in retarget directory: {0}. Will be skipped during standard retargeting.'.format(fullPath))
                else:
                    texDb[lowCaseFilename] = fullPath
        return texDb


class ProcessorCopyMove(ProcessorBase):

    def __init__(self, filenames, targetRoot, delSrc, copyFolderStruct, sourceRoot, copyAdd, addSuffixes):
        super(ProcessorCopyMove, self).__init__()

        self.filenames = filenames
        self.targetRoot = targetRoot
        self.delSrc = delSrc
        self.copyFolderStruct = copyFolderStruct
        self.sourceRoot = sourceRoot
        self.copyAdd = copyAdd
        self.addSuffixes = addSuffixes

        self.processedInfo = {}

    def execute(self):
        filesToProcess = self.getFilesToProcess()

        if self.copyFolderStruct:
            copyInfo = self.getCopyInfoFolderStructure(filesToProcess)
        else:
            copyInfo = self.getCopyInfoSimple(filesToProcess)

        checkedDirs = set()
        createdDirs = set()
        for s, t in copyInfo:
            targetDir = os.path.dirname(t)
            if targetDir not in checkedDirs:
                checkedDirs.add(targetDir)
                if not os.path.exists(targetDir):
                    try:
                        os.makedirs(targetDir)
                        createdDirs.add(targetDir)
                    except os.error as e:
                        self.log(str(e))
                else:
                    createdDirs.add(targetDir)

            if targetDir in createdDirs:
                try:
                    makeWritable(t)
                    shutil.copy(s, t)
                    self.processedInfo[s.lower()] = t
                except IOError as e:
                    self.log(str(e))

        if self.delSrc:
            for f in self.processedInfo:
                if os.path.exists(f):
                    try:
                        makeWritable(f)
                        os.remove(f)
                    except OSError as e:
                        self.log(str(e))

    def getCopyInfoSimple(self, files):
        return [(f, '{0}/{1}'.format(self.targetRoot, os.path.basename(f))) for f in files]

    def getCopyInfoFolderStructure(self, files):
        res = []
        for f in files:
            srcLower = self.sourceRoot.lower() + '/'
            if f.lower().startswith(srcLower):
                res.append((f, '{0}/{1}'.format(self.targetRoot, f[len(srcLower):])))
            else:
                trgF = f
                for r in ('//', ':', '$'):
                    trgF = trgF.replace(r, '')
                res.append((f, '{0}/{1}'.format(self.targetRoot, trgF)))
        return res

    def getFilesToProcess(self):
        filesDict = {}

        for f in self.filenames:
            f = os.path.expandvars(f)
            fLower = f.lower()
            if fLower not in filesDict:
                if os.path.exists(f):
                    filesDict[fLower] = f

                    fNoExt, ext = os.path.splitext(f)
                    for suf in self.addSuffixes:
                        addFilename = '{0}{1}{2}'.format(fNoExt, suf, ext)
                        addFilenameLower = addFilename.lower()
                        if addFilenameLower not in filesDict:
                            if os.path.exists(addFilename):
                                filesDict[addFilenameLower] = addFilename

        return sorted(filesDict.values())


class ProcessorCopyMoveUI(ProcessorCopyMove):

    def __init__(self, tns, targetRoot, retarget, delSrc, copyFolderStruct, sourceRoot, copyAdd, addSuffixes):
        super(ProcessorCopyMoveUI, self).__init__(
            [tn.getAttrValue() for tn in tns],
            targetRoot,
            delSrc,
            copyFolderStruct,
            sourceRoot,
            copyAdd,
            addSuffixes
        )
        self.tns = tns
        self.retarget = retarget
        
    def execute(self):
        super(ProcessorCopyMoveUI, self).execute()

        if self.retarget:
            for tn in self.tns:
                oldValue = os.path.expandvars(tn.getAttrValue()).lower()
                if oldValue in self.processedInfo:
                    tn.setAttrValue(self.processedInfo[oldValue])
