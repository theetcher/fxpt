from fxpt.fx_refSystem.fx_references import getActiveRefHandles, deactivateRefs, activateRefs, cleanupReferences, makeRefsPathRelative


gPresaveActiveRefHandles = []


# noinspection PyUnusedLocal
def preSaveProcedure(callbackArg):
    global gPresaveActiveRefHandles
    gPresaveActiveRefHandles = getActiveRefHandles()
    deactivateRefs(gPresaveActiveRefHandles)
    # cleanupReferences()  # deactivation and cleanup. something wrong. after that it does not activate back...

    makeRefsPathRelative()


# noinspection PyUnusedLocal
def postSaveProcedure(callbackArg):
    activateRefs(gPresaveActiveRefHandles)


# noinspection PyUnusedLocal
def preExportProcedure(callbackArg):
    pass


# noinspection PyUnusedLocal
def postOpenProcedure(callbackArg):
    cleanupReferences()
    makeRefsPathRelative()
