import os
import maya.cmds as m

ENV_VARS = (
    'MAYA_APP_DIR',
    'MAYA_LOCATION',
    'MAYA_SCRIPT_PATH',
    'PYTHONPATH',
    'MAYA_MODULE_PATH',
    'MAYA_PLUG_IN_PATH',
    'MAYA_SHELF_PATH',
    'PATH',
    'TMPDIR',
    'XBMLANGPATH'
)

INTERNAL_VARS = (
    'userAppDir',
    'userScriptDir',
    'userPrefDir',
    'userPresetsDir',
    'userShelfDir',
    'userMarkingMenuDir',
    'userBitmapsDir',
    'userTmpDir',
    'userWorkspaceDir',
    'userHotkeyDir'
)

OFFSET = '    '


def run():
    print
    print '--- ENVIRONMENT VARIABLES ---'
    print
    for env in ENV_VARS:
        print env
        value = os.environ.get(env, None)
        if value is None:
            print OFFSET + 'variable not set.'
        else:
            for p in value.split(';'):
                print OFFSET + p.strip()

    print
    print '--- INTERNAL VARIABLES ---'
    print
    for kwarg in INTERNAL_VARS:
        print kwarg
        value = m.internalVar(**{kwarg: True}).strip()
        if not value:
            print OFFSET + 'variable not set.'
        else:
            for p in value.split(';'):
                print OFFSET + p.strip()
