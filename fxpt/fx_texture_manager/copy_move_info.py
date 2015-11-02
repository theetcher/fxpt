from collections import namedtuple

CopyMoveInfo = namedtuple(
    'CopyMoveInfo',
    (
        'targetRoot',
        'retarget',
        'delSrc',
        'copyFolderStruct',
        'sourceRoot',
        'copyAdd',
        'addSuffixes'
    )
)
