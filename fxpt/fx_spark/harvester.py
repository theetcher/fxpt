import inspect
import types
import json

import maya.cmds as m

from . import command_desc, cfg

# from fxpt.fx_utils.watch import watch


class Harvester(object):
    def __init__(self):
        self.db = {
            cfg.SEARCH_CATEGORY_TOOLS: {},
            cfg.SEARCH_CATEGORY_CMD: {},
            cfg.SEARCH_CATEGORY_CMD_RT: {},
            cfg.SEARCH_CATEGORY_ALL: {}
        }

    def harvest(self):
        self.harvestCommands()
        self.harvestCommandsRt()
        self.harvestTools()
        self.harvestAll()
        return self.db

    def harvestCommands(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_CMD]
        mayaCommands = [n for n, t in inspect.getmembers(m) if isinstance(t, types.BuiltinFunctionType)]
        for cmd in mayaCommands:
            cd = command_desc.CommandDesc(cmd)
            cd.run = cmd
            catDb[cmd.lower()] = cd

        # for key, value in catDb.items():
        #     print key, '>>>', value

    def harvestCommandsRt(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_CMD_RT]

        for cmd in sorted(m.runTimeCommand(q=True, commandArray=True)):
            annotation = m.runTimeCommand(cmd, q=True, annotation=True)
            # category = m.runTimeCommand(c, q=True, category=True)
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

        # for key, value in catDb.items():
        #     print key, '>>>', value

    def harvestTools(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_TOOLS]

        with open(cfg.TOOLS_CFG, 'r') as f:
            toolsJsonObj = json.load(f)
        for rec in toolsJsonObj:
            cd = command_desc.CommandDesc(rec['name'])
            cd.run = rec['run']
            cd.annotation = rec['annotation']
            catDb[cd.name.lower()] = cd

        # for key, value in catDb.items():
        #     print key, '>>>', value

    def harvestAll(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_ALL]

        for dbKey in cfg.SEARCHES_WITHOUT_ALL:
            catDb.update(self.db[dbKey])

        # for key, value in catDb.items():
        #     print key, '>>>', value

