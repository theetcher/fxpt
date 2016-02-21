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
UI_FRAME_CENTER_OFFSET = -200
UI_ITEM_SIZE = 24
UI_LIST_SIZE_BOTTOM_MARGIN = 0
UI_MAX_RESULTS_HEIGHT = 300
UI_CONTENTS_MARGIN = 4
UI_LABEL_HEIGHT = 30
UI_SEARCH_FIELD_HEIGHT = 28

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
TOOL_CFG_FIELD_MEL = 'mel'
TOOL_CFG_FIELD_PYTHON = 'python'
TOOL_CFG_FIELD_ANNOTATION = 'annotation'

BUILT_IN_TOOLS = [
    {
        TOOL_CFG_FIELD_NAME: 'Spark Configuration Directory',
        TOOL_CFG_FIELD_PYTHON: 'from fxpt.fx_spark import spark_config; spark_config.run()',
        TOOL_CFG_FIELD_ANNOTATION: 'Open Spark Configuration Directory',
    }
]

TOOLS_CFG_USER_DEFAULT = '''
- name: Print Maya.env Location
  mel: print(`about -environmentFile`)
  annotation: Print maya.env location

- name: Print MAYA_APP_DIR
  python: import os; print os.environ.get('MAYA_APP_DIR', None)
  annotation: Print MAYA_APP_DIR environment variable
'''

STYLE_SHEET = '''
.QFrame {
    background-color: #333333;
    border-radius: 4px;
    }

QLabel {
    color: #aaaaaa;
    font: normal italic 14px "Segoi UI";
    margin: 0px;
    padding: 0px 8px 0px 8px;
    }

QLineEdit {
    color: black;
    background-color: #ffa000;
    border-radius: 2px;
    margin: 0px 4px 0px 4px;
    padding: 0px 6px 0px 6px;
    font: normal normal 16px;
    }

QListWidget {
    background-color: #333333;
    border: 0px;
    font: normal normal 14px;
    margin: 0px 4px 0px 4px;
    alternate-background-color: #2f2f2f;
    outline: none;
    }

QListView::item:hover {
    color: white;
    background-color: #333333;
}

QListView::item:selected {
    border-radius: 2px;
    padding: 0px 4px 0px 4px;
    background-color: #444444;
}
'''
