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
        return procSearchReplace.getLog()

    # noinspection PyMethodMayBeStatic
    def processRetarget(self, *args):
        procRetarget = Processors.ProcessorRetarget(*args)
        procRetarget.execute()
        return procRetarget.getLog()

    # noinspection PyMethodMayBeStatic
    def processCopyMove(self, tns, dlgResult):
        procCopyMove = Processors.ProcessorCopyMoveUI(
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


