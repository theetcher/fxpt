import sys
import os
import inspect
import sysconfig
from importlib import reload

from types import ModuleType

SCRIPT_NAME = 'rreload'
DEBUG_LOG_TITLE = '#' + SCRIPT_NAME + ': '

_processedModules = set()
_reloadedModules = set()
_remappingData = list()

_verbosity = 0
_debugOffset = 0
_debugOffsetString = ''

TAB_SIZE = 4

IGNORE_DIRECTORIES = [
    sysconfig.get_path('stdlib').lower(),
    'autodesk\\maya',
    'pythonpackages',
    'pyqt',
    'keyring',
]


def debugLog(*args, **kwargs):
    verbosity = kwargs.get('verbosity', 1)
    title = kwargs.get('title', True)
    if verbosity <= _verbosity:
        #TODO: ugly
        print((DEBUG_LOG_TITLE if title else '') + _debugOffsetString + ''.join(args))


def debugLogEmpty():
    debugLog('', verbosity=1, title=True)


def changeDbgOffset(amount):
    global _debugOffset, _debugOffsetString
    _debugOffset += amount
    _debugOffsetString = ('|' + ' ' * (TAB_SIZE - 1)) * _debugOffset


def needToBeIgnored(moduleFilename):
    # This is original check for builtin path. Not valid if run in Maya.

    # pyStdLib = sysconfig.get_python_lib(standard_lib=True).lower()
    # pySitePkg = sysconfig.get_python_lib().lower()
    # if moduleFilepath.startswith(pyStdLib) and (not moduleFilepath.startswith(pySitePkg)):
    #     continue

    moduleDir = os.path.dirname(moduleFilename).lower()
    for s in IGNORE_DIRECTORIES:
        if s in moduleDir:
            return True
    return False


class ImportRemapData(object):

    def __init__(
            self,
            destModuleName,
            destAttrName,
            sourceModuleName,
            sourceAttrName,
            attrType
    ):

        self._destModuleName = destModuleName
        self._destAttrName = destAttrName
        self._sourceModuleName = sourceModuleName
        self._sourceAttrName = sourceAttrName
        self._attrType = attrType

    def remap(self):
        sourceModule = sys.modules[self._sourceModuleName]

        if self._attrType == ModuleType:
            newAttrVal = sys.modules[self._sourceAttrName]
        else:
            newAttrVal = getattr(sourceModule, self._sourceAttrName)

        destModule = sys.modules[self._destModuleName]
        setattr(destModule, self._destAttrName, newAttrVal)


def rreload(module, remapping=False, verbosity=0):

    global _verbosity
    _verbosity = verbosity

    debugLogEmpty()
    debugLog('RELOAD STARTED.', verbosity=1)

    doReload(module, remapping=remapping)

    if remapping:
        debugLog('remapping process begins...', verbosity=1)
        for remapData in _remappingData:
            remapData.remap()
        debugLog('remapping done.', verbosity=1)
    else:
        debugLog('remapping skipped.', verbosity=1)

    _processedModules.clear()
    _reloadedModules.clear()
    del _remappingData[:]

    debugLog('RELOAD FINISHED.', verbosity=1)
    debugLog('', verbosity=1, title=False)


def doReload(module, remapping=False):

    changeDbgOffset(1)

    debugLogEmpty()
    debugLog(module.__name__, ': START PROCESSING.', verbosity=1)
    debugLogEmpty()

    _processedModules.add(module)

    attrNames = dir(module)
    attrCount = len(attrNames)

    detectedModules = set()

    dbgPhaseTitle = module.__name__ + ': attribute analyzing phase: '
    debugLog(dbgPhaseTitle, 'analyzing ', str(attrCount), ' module attributes.', verbosity=1)

    for attrName in attrNames:

        attrVal = getattr(module, attrName)
        attrModule = inspect.getmodule(attrVal)

        if not attrModule:
            debugLog(dbgPhaseTitle, '"', attrName, '"(attr): cannot get module for attribute. Skipped.', verbosity=2)
            continue

        debugLog(dbgPhaseTitle, '"', attrName, '"(attr): attribute belongs to module "', attrModule.__name__, '"', verbosity=2)

        if attrModule.__name__ in sys.builtin_module_names:
            debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): builtin. Skipped.', verbosity=2)
            continue

        if not hasattr(attrModule, '__file__'):
            debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): no "__file__" attribute. Skipped.', verbosity=2)
            continue

        if attrModule == sys.modules[__name__]:
            debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): ', SCRIPT_NAME, ' itself. Skipped.', verbosity=2)
            continue

        if attrModule in _processedModules:
            debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): already processed. Skipped.', verbosity=2)
            continue

        if needToBeIgnored(attrModule.__file__.lower()):
            debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): in ignore list. Skipped.', verbosity=2)
            continue

        detectedModules.add(attrModule)
        debugLog(dbgPhaseTitle, '"', attrModule.__name__, '"(module): added to list of detected modules.', verbosity=2)

        if remapping:

            if not hasattr(attrVal, '__name__'):
                continue

            origName = attrVal.__name__

            if attrModule != module:
                debugLog(' '.join((dbgPhaseTitle + 'preparing mapping data:', module.__name__, attrName, '<-',
                                   attrModule.__name__, origName, str(type(attrVal)))), verbosity=2)
                remapData = ImportRemapData(
                    module.__name__,
                    attrName,
                    attrModule.__name__,
                    origName,
                    type(attrVal)
                )
                _remappingData.append(remapData)

    if _verbosity > 0:
        dbgPhaseTitle = module.__name__ + ': detected modules summary: '
        debugLogEmpty()
        if detectedModules:
            debugLog(dbgPhaseTitle, 'following modules must be processed:', verbosity=1)
            for md in detectedModules:
                debugLog(md.__name__,)
        else:
            debugLog(dbgPhaseTitle, 'no modules to process.', verbosity=1)

    debugLogEmpty()

    dbgPhaseTitle = module.__name__ + ': recursion entrance phase: '
    for detectedModule in detectedModules:
        if detectedModule in _reloadedModules:
            debugLog(dbgPhaseTitle, 'module "' + detectedModule.__name__ + '" was already reloaded. Skipping recursion.', verbosity=1)
            continue
        debugLog(dbgPhaseTitle, 'module "' + detectedModule.__name__ + '" is not analyzed. Entering recursion.', verbosity=1)
        doReload(detectedModule)

    dbgPhaseTitle = module.__name__ + ': reload phase: '
    if module.__name__ != '__main__':
        debugLog(dbgPhaseTitle, 'reloading module "' + module.__name__ + '".', verbosity=1)
        reload(module)
        _reloadedModules.add(module)
    else:
        debugLog(dbgPhaseTitle, 'cannot reload "__main__" module. Skipped', verbosity=1)

    debugLogEmpty()
    debugLog(module.__name__, ': PROCESSING FINISHED.', verbosity=1)
    debugLogEmpty()

    changeDbgOffset(-1)
