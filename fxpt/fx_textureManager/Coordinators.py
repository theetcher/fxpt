from fxpt.fx_textureManager import Processors


class CoordinatorMayaUI(object):

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def processPaste(self, *args):
        procPaste = Processors.ProcessorPaste(*args)
        procPaste.execute()

    # noinspection PyMethodMayBeStatic
    def processSearchAndReplace(self, *args):
        procSearchReplace = Processors.ProcessorSearchReplace(*args)
        procSearchReplace.execute()

    # noinspection PyMethodMayBeStatic
    def processRetarget(self, *args):
        procRetarget = Processors.ProcessorRetarget(*args)
        procRetarget.execute()

    # noinspection PyMethodMayBeStatic
    def processCopyMove(self, tns, dlgResult):
        print '--- processCopyMove args ---'
        # noinspection PyProtectedMember
        for key, value in dlgResult._asdict().iteritems():
            print '{0}={1},'.format(key, value)

        processors = []

        procCopyMove = Processors.ProcessorCopyMoveUI(
            tns,
            dlgResult.targetRoot,
            dlgResult.delSrc,
            dlgResult.copyFolderStruct,
            dlgResult.sourceRoot,
            dlgResult.copyAdd,
            dlgResult.addSuffixes,
        )
        processors.append(procCopyMove)

        if dlgResult.retarget:
            procRetarget = Processors.ProcessorRetarget(tns, dlgResult.targetRoot, dlgResult.forceRetarget)
            processors.append(procRetarget)

        for proc in processors:
            proc.execute()


