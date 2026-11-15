import maya.cmds as m
import maya.OpenMaya as om

from fxpt3.fx_refsystem.fx_references import preSaveProcedure, postSaveProcedure, postOpenProcedure
from fxpt3.fx_refsystem.roots_cfg_handler import RootsCfgHandler

callbackIds = []


def init():
    # safe to call more than once: drop callbacks from a previous init() first
    uninit()

    callbackIds.append(om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, preSaveProcedure))
    callbackIds.append(om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave, postSaveProcedure))
    callbackIds.append(om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, postOpenProcedure))
    # om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeExport, saveJobs.preExportProcedure)

    m.setNodeTypeFlag('unknownTransform', display=False)  # to hide reference source group from outliner

    RootsCfgHandler().setEnvVar()


def uninit():
    while callbackIds:
        om.MMessage.removeCallback(callbackIds.pop())
