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

    def processCopyMove(self, tns, dlgResult):
        # noinspection PyProtectedMember
        for key, value in dlgResult._asdict().iteritems():
            print '{0}={1},'.format(key, value)
