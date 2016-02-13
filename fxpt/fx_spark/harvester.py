import os
import inspect
import types

import maya.cmds as m

from . import command_desc, cfg, yaml_io
from fxpt.fx_utils import message_box


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
        self.harvestAll()
        self.harvestHelp()
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

    # noinspection PyMethodMayBeStatic
    def getToolsList(self, filename):
        try:
            l = yaml_io.load(filename, silent=True)
        except StandardError:
            l = []
        return l

    # noinspection PyMethodMayBeStatic
    def isValidToolDefinition(self, rec):
        for f in cfg.TOOL_CFG_MANDATORY_FIELDS:
            if f not in rec:
                return False
            if not isinstance(rec[f], str):
                return False
        return True

    # noinspection PyMethodMayBeStatic
    def generateBuiltInCommands(self, catDb):
        for rec in cfg.BUILT_IN_TOOLS:
            cd = command_desc.CommandDesc(rec[cfg.TOOL_CFG_FIELD_NAME])
            cd.run = rec[cfg.TOOL_CFG_FIELD_RUN]
            cd.annotation = rec[cfg.TOOL_CFG_FIELD_ANNOTATION]
            catDb[cd.name.lower()] = cd

    # noinspection PyMethodMayBeStatic
    def createUserToolsList(self):
        if not os.path.exists(cfg.SPARK_USER_CFG_DIR):
            os.makedirs(cfg.SPARK_USER_CFG_DIR)
        if not os.path.exists(cfg.TOOLS_CFG_USER):
            with open(cfg.TOOLS_CFG_USER, 'w') as f:
                f.write(cfg.TOOLS_CFG_USER_DEFAULT)

    def harvestTools(self):
        self.createUserToolsList()

        catDb = self.db[cfg.SEARCH_CATEGORY_TOOLS]

        self.generateBuiltInCommands(catDb)

        for toolsConfig in [cfg.TOOLS_CFG, cfg.TOOLS_CFG_USER]:
            toolsList = self.getToolsList(toolsConfig)

            for rec in toolsList:
                if not self.isValidToolDefinition(rec):
                    message_box.warning('Found bad tool definition in\n{}\nIgnored.'.format(toolsConfig), textDetailed=str(rec))
                    continue

                cd = command_desc.CommandDesc(rec[cfg.TOOL_CFG_FIELD_NAME].strip())
                cd.run = rec[cfg.TOOL_CFG_FIELD_RUN].strip()
                cd.annotation = rec[cfg.TOOL_CFG_FIELD_ANNOTATION].strip()
                if not cd.annotation:
                    cd.annotation = cd.name
                nameL = cd.name.lower()

                if nameL in catDb or \
                        nameL in self.db[cfg.SEARCH_CATEGORY_CMD] or \
                        nameL in self.db[cfg.SEARCH_CATEGORY_CMD_RT]:
                    message_box.warning('Cannot add tool "{}" defined in:\n{}\nThat name already exists.'.format(cd.name, toolsConfig))
                    continue

                catDb[nameL] = cd

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
