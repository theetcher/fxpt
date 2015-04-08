import maya.cmds as m
import maya.OpenMaya as om

from fxpt.fx_refSystem import saveJobs


def refUserSetup():
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, saveJobs.preSaveProcedure)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, saveJobs.postSaveProcedure)
    # om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeExport, saveJobs.preExportProcedure)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, saveJobs.postOpenProcedure)

    m.setNodeTypeFlag('unknownTransform', display=False)  # to hide reference source group from outliner
