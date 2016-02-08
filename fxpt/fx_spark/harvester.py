import inspect
import types

import maya.cmds as m

from . import command_desc, cfg, json_io

# from fxpt.fx_utils.watch import watch


class Harvester(object):
    def __init__(self):
        self.db = {
            cfg.SEARCH_CATEGORY_TOOLS: {},
            cfg.SEARCH_CATEGORY_CMD: {},
            cfg.SEARCH_CATEGORY_CMD_RT: {},
            cfg.SEARCH_CATEGORY_HELP: {},
            cfg.SEARCH_CATEGORY_ALL: {}
        }

    def harvest(self):
        self.harvestCommands()
        self.harvestCommandsRt()
        self.harvestTools()
        self.harvestHelp()
        self.harvestAll()
        return self.db

    def harvestCommands(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_CMD]
        mayaCommands = [n for n, t in inspect.getmembers(m) if isinstance(t, types.BuiltinFunctionType)]
        for cmd in mayaCommands:
            cd = command_desc.CommandDesc(cmd)
            cd.run = cmd
            cd.annotation = 'Maya Command: ' + cmd
            catDb[cmd.lower()] = cd

    def harvestCommandsRt(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_CMD_RT]

        for cmd in sorted(m.runTimeCommand(q=True, commandArray=True)):
            annotation = m.runTimeCommand(cmd, q=True, annotation=True).strip()
            if not annotation:
                annotation = cmd
            annotationL = annotation.lower()
            cmdL = cmd.lower()
            if '(press)' in annotationL \
                    or '(release)' in annotationL or \
                    cmdL.endswith('press') or \
                    cmdL.endswith('release'):
                continue

            cd = command_desc.CommandDesc(cmd)
            cd.run = cmd
            cd.annotation = annotation
            catDb[cmdL] = cd

    def harvestTools(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_TOOLS]

        try:
            toolsJsonObj = json_io.load(cfg.TOOLS_CFG)
        except StandardError:
            toolsJsonObj = []

        for rec in toolsJsonObj:
            cd = command_desc.CommandDesc(rec['name'].strip())
            cd.run = rec['run'].strip()
            annotation = rec['annotation'].strip()
            if not annotation:
                annotation = rec['name']
            cd.annotation = annotation
            catDb[cd.name.lower()] = cd

    def harvestHelp(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_HELP]

        for line in cfg.HELP_LINES:
            cd = command_desc.CommandDesc(line)
            cd.annotation = cfg.UI_DEFAULT_ANNOTATION
            catDb[line.lower()] = cd

    def harvestAll(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_ALL]

        for dbKey in cfg.SEARCHES_TYPES_ALL:
            catDb.update(self.db[dbKey])

