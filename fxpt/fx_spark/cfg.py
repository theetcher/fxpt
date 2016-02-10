import os
import maya.cmds as m

from fxpt.fx_utils.utils import pathToSlash, getUserCfgDir


MAYA_VERSION = m.about(version=True)
TOOL_DIR = pathToSlash(os.path.dirname(__file__))
TOOLS_CFG = TOOL_DIR + '/tools_list.yaml'
SPARK_USER_CFG_DIR = getUserCfgDir() + '/fx_spark'
TOOLS_CFG_USER = SPARK_USER_CFG_DIR + '/tools_list_user.yaml'
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

UI_DEFAULT_ANNOTATION = 'Type something to search or type ? to help'
UI_DEFAULT_STATUS = 'Favorite and Recent commands:'

SEARCH_CATEGORY_TOOLS = 'tools'
SEARCH_CATEGORY_CMD = '@'
SEARCH_CATEGORY_CMD_RT = '#'
SEARCH_CATEGORY_ALL = '!'
SEARCH_CATEGORY_HELP = '?'

HELP_LINES = (
    '1. Start typing to search in Spark tools.',
    '2. Type @ to search in Maya Commands.',
    '3. Type # to search in Maya Runtime Commands.',
    '4. Type ! to search everywhere.',
    '5. Run SparkCfgDir command to open configuration directory.'
)

SPECIAL_SEARCHES = {SEARCH_CATEGORY_CMD, SEARCH_CATEGORY_CMD_RT, SEARCH_CATEGORY_HELP, SEARCH_CATEGORY_ALL}
SEARCHES_TYPES_ALL = {SEARCH_CATEGORY_CMD, SEARCH_CATEGORY_CMD_RT, SEARCH_CATEGORY_TOOLS}

TOOL_CFG_FIELD_NAME = 'name'
TOOL_CFG_FIELD_RUN = 'run'
TOOL_CFG_FIELD_ANNOTATION = 'annotation'

TOOL_CFG_MANDATORY_FIELDS = [
    TOOL_CFG_FIELD_NAME,
    TOOL_CFG_FIELD_RUN,
    TOOL_CFG_FIELD_ANNOTATION
]

BUILT_IN_TOOLS = [
    {
        TOOL_CFG_FIELD_NAME: 'SparkCfgDir',
        TOOL_CFG_FIELD_RUN: 'python("from fxpt.fx_spark import spark_config; spark_config.run()")',
        TOOL_CFG_FIELD_ANNOTATION: 'Open Spark Configuration Directory',
    }
]

TOOLS_CFG_USER_DEFAULT = '''
- name: Hello World (MEL)
  run: print("Hello World!\\n")
  annotation: Hello World MEL command.

- name: Hello World (Python)
  run: python("print 'Hello World!\\\\n',")
  annotation: Hello World Python command.

'''

# TOOLS_CFG_USER_DEFAULT = '''
# - name: Number of Selected Nodes
#   run: print(size(`selectedNodes`)+" node(s) selected\\n");
#   annotation: Prints number of selected nodes
# '''
