import os

import maya.cmds as m

SCRIPT_DIR = os.path.dirname(__file__)


from fxpt.fx_textureManager.Harvesters import MayaSceneHarvester
from fxpt.fx_textureManager.Processors import ProcessorPaste, ProcessorCopyMoveUI


def runPaste():
    sceneName = SCRIPT_DIR + '/testMayaProject/scenes/testScene_04.mb'
    saveSceneName = SCRIPT_DIR + '/testMayaProject/scenes/testScene_04_processed.mb'

    m.file(sceneName, o=True, f=True, typ='mayaBinary', options='v=0;')

    harvester = MayaSceneHarvester()
    tns = harvester.getTexNodes()

    proc = ProcessorPaste(tns, 'aaa')
    proc.execute()

    m.file(rename=saveSceneName)
    m.file(f=True, save=True, options='v=0;', typ='mayaBinary')


def runCopyMove():
    sceneName = SCRIPT_DIR + '/testMayaProject/scenes/testScene_04.mb'
    saveSceneName = SCRIPT_DIR + '/testMayaProject/scenes/testScene_04_processed.mb'

    m.file(sceneName, o=True, f=True, typ='mayaBinary', options='v=0;')

    harvester = MayaSceneHarvester()
    tns = harvester.getTexNodes()

    proc = ProcessorCopyMoveUI(
        tns=tns,
        targetRoot='C:\__test__',
        retarget=True,
        delSrc=False,
        copyFolderStruct=True,
        sourceRoot='',
        copyAdd=False,
        addSuffixes=''
    )
    proc.execute()

    m.file(rename=saveSceneName)
    m.file(f=True, save=True, options='v=0;', typ='mayaBinary')