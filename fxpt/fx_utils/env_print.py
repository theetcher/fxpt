import os

ENV_VARS = (
    'MAYA_APP_DIR',
    'MAYA_LOCATION',
    'MAYA_SCRIPT_PATH',
    'PYTHONPATH',
    'MAYA_MODULE_PATH',
    'MAYA_PLUG_IN_PATH',
    'PATH',
    'TMPDIR',
    'XBMLANGPATH'
)

OFFSET = '    '


def run():
    print
    for env in ENV_VARS:
        print env
        value = os.environ.get(env, None)
        if value is None:
            print OFFSET + 'variable not set.'
        else:
            for p in sorted(value.split(';')):
                print OFFSET + p.strip()
