import maya.cmds as m
import maya.OpenMaya as om

from fxpt.fx_refSystem.fx_references import preSaveProcedure, postSaveProcedure, postOpenProcedure
from fxpt.fx_refSystem.roots_cfg_handler import RootsCfgHandler


def init():
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, preSaveProcedure)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, postSaveProcedure)
    om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, postOpenProcedure)
    # om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeExport, saveJobs.preExportProcedure)

    m.setNodeTypeFlag('unknownTransform', display=False)  # to hide reference source group from outliner

    RootsCfgHandler().setEnvVar()