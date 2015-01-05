from fxpt.fx_textureManager import Processors


class CoordinatorMayaUI(object):

    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def processPaste(self, tns, newFilename):
        procPaste = Processors.ProcessorPaste(tns, newFilename)
        procPaste.execute()

    # noinspection PyMethodMayBeStatic
    def processSearchAndReplace(self, tns, oldStr, newStr):
        procSearchReplace = Processors.ProcessorSearchReplace(tns, oldStr, newStr)
        procSearchReplace.execute()
