from fxpt3.fx_texture_manager import processors


class CoordinatorMayaUI(object):

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def processPaste(self, *args):
        procPaste = processors.ProcessorPaste(*args)
        procPaste.execute()

    # noinspection PyMethodMayBeStatic
    def processSearchAndReplace(self, *args):
        procSearchReplace = processors.ProcessorSearchReplace(*args)
        procSearchReplace.execute()
        return procSearchReplace.getLog()

    # noinspection PyMethodMayBeStatic
    def processRetarget(self, *args):
        procRetarget = processors.ProcessorRetarget(*args)
        procRetarget.execute()
        return procRetarget.getLog()

    # noinspection PyMethodMayBeStatic
    def processCopyMove(self, tns, dlgResult):
        procCopyMove = processors.ProcessorCopyMoveUI(
            tns,
            dlgResult.targetRoot,
            dlgResult.retarget,
            dlgResult.delSrc,
            dlgResult.copyFolderStruct,
            dlgResult.sourceRoot,
            dlgResult.copyAdd,
            dlgResult.addSuffixes,
        )
        procCopyMove.execute()
        return procCopyMove.getLog()


