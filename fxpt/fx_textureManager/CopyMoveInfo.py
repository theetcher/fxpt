from collections import namedtuple

CopyMoveInfo = namedtuple(
    'CopyMoveInfo',
    (
        'targetRoot',
        'delSrc',
        'copyFolderStruct',
        'sourceRoot',
        'copyAdd',
        'addSuffixes',
        'retarget',
        'forceRetarget'
    )
)
