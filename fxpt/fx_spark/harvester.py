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
            cd = command_desc.CommandDescMel(cmd)
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

            cd = command_desc.CommandDescMel(cmd)
            cd.run = cmd
            cd.annotation = annotation
            catDb[cmdL] = cd

    # noinspection PyMethodMayBeStatic
    def getToolsList(self, filename):
        try:
            l = yaml_io.load(filename, alertNotExist=False)
        except StandardError:
            l = []
        return l

    # noinspection PyMethodMayBeStatic
    def getRecValue(self, rec, fieldName):
        value = rec.get(fieldName, None)
        if value is None:
            return ''
        if not isinstance(value, str):
            message_box.warning(
                'Bad type for field "{}". Only "str" allowed. Replaced with empty string.'.format(fieldName),
                textDetailed=str(rec)
            )
            return ''
        return value.strip()

    def createCommandDesc(self, rec):
        name = self.getRecValue(rec, cfg.TOOL_CFG_FIELD_NAME)
        if not name:
            message_box.warning(
                'Tools without names not allowed. Skipped.',
                textDetailed=str(rec)
            )
            return
        mel = self.getRecValue(rec, cfg.TOOL_CFG_FIELD_MEL)
        python = self.getRecValue(rec, cfg.TOOL_CFG_FIELD_PYTHON)
        if mel and python:
            message_box.warning(
                'Both "mel" and "python" fields present in tool. Provide only one.',
                textDetailed=str(rec)
            )
            return
        annotation = self.getRecValue(rec, cfg.TOOL_CFG_FIELD_ANNOTATION)

        if python:
            cd = command_desc.CommandDescPython(name)
            cd.run = python
        else:
            cd = command_desc.CommandDescMel(name)
            cd.run = mel
        cd.annotation = annotation

        return cd

    # noinspection PyMethodMayBeStatic
    def generateBuiltInCommands(self, catDb):
        for rec in cfg.BUILT_IN_TOOLS:
            cd = self.createCommandDesc(rec)
            if not cd:
                return
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
                cd = self.createCommandDesc(rec)
                if not cd:
                    continue

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
            cd = command_desc.CommandDescMel(line)
            cd.annotation = cfg.UI_DEFAULT_ANNOTATION
            catDb[line.lower()] = cd

    def harvestAll(self):
        catDb = self.db[cfg.SEARCH_CATEGORY_ALL]

        for dbKey in cfg.SEARCHES_TYPES_ALL:
            catDb.update(self.db[dbKey])
