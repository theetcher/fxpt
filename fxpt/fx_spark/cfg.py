import os
import maya.cmds as m

from fxpt.fx_utils.utils import pathToSlash


MAYA_VERSION = m.about(version=True)
TOOL_DIR = pathToSlash(os.path.dirname(__file__))
# TODO: think about safe location of TOOLS_CFG location (%APPDATA% ?)
# TODO: how to override this path (tools_list.path near orig with path in first line to new location?). or maybe full scope tool yaml cfg ?? with override to path ?
# TODO: YAML as config ?????
# TODO: initial config ? generate something like About MEL, About Python, Create Locator, ...
# TODO: Cog button to open cfg location dir?
TOOLS_CFG = TOOL_DIR + '/tools_list.json'
HISTORY_FILE = TOOL_DIR + '/history.json'

HISTORY_LENGTH = 5

UI_FRAME_WIDTH = 500
UI_FRAME_CENTER_OFFSET = -100
UI_ITEM_SIZE = 18
UI_LIST_SIZE_BOTTOM_MARGIN = 4
UI_MAX_RESULTS_HEIGHT = 300
UI_CONTENTS_MARGIN = 8
UI_SPACING = 4
UI_LABEL_HEIGHT = 20
UI_SEARCH_FIELD_HEIGHT = 20

UI_DEFAULT_ANNOTATION = 'Type ? to help'
UI_DEFAULT_STATUS = 'Favorite and Recent commands:'

SEARCH_CATEGORY_TOOLS = 'tools'
SEARCH_CATEGORY_CMD = '@'
SEARCH_CATEGORY_CMD_RT = '#'
SEARCH_CATEGORY_ALL = '!'
SEARCH_CATEGORY_HELP = '?'

HELP_LINES = (
    'Start typing to search in Spark tools.',
    'Type @ to search in Maya Commands.',
    'Type # to search in Maya Runtime Commands.',
    'Type ! to search everywhere.'
)

SPECIAL_SEARCHES = {SEARCH_CATEGORY_CMD, SEARCH_CATEGORY_CMD_RT, SEARCH_CATEGORY_HELP, SEARCH_CATEGORY_ALL}
SEARCHES_TYPES_ALL = {SEARCH_CATEGORY_CMD, SEARCH_CATEGORY_CMD_RT, SEARCH_CATEGORY_TOOLS}
