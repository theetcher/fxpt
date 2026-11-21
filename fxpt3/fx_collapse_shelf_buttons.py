# Shows and hides groups of shelf buttons with a toggle button on the same shelf.
#
# Mark each button of a group with a comment in its command (the group name is followed by whitespace or the end):
#   Python: # fx_collapse_shelf_buttons.collapse_group = group_name
#   MEL:    // fx_collapse_shelf_buttons.collapse_group = group_name
#
# The toggle button command (Python):
#   from fxpt3 import fx_collapse_shelf_buttons; fx_collapse_shelf_buttons.toggle('shelf_name', 'group_name')
#
# To restore saved states at Maya startup (e.g. from userSetup, deferred until the UI exists):
#   from fxpt3 import fx_collapse_shelf_buttons; fx_collapse_shelf_buttons.initCollapse()

import re

import maya.mel as mel
import maya.cmds as m

OPT_VAR_PREFIX = 'fx_collapse_shelf_buttons_'

IMAGE_OPENED = 'collapseBarOpened.png'
IMAGE_CLOSED = 'collapseBarClosed.png'

TOGGLE_RE = re.compile(r"fx_collapse_shelf_buttons\.toggle\(\s*'(.*?)'\s*,\s*'(.*?)'\s*\)")


def toggle(shelf, group):
    state = toggleState(getSavedState(shelf, group))
    setGroupState(shelf, group, state)
    saveState(shelf, group, state)


def toggleState(state):
    return 1 if state == 0 else 0


def setGroupState(shelf, group, state):
    if shelf not in getShelves():
        m.warning('Cannot find shelf "' + shelf + '".')
        return

    groupRe = re.compile(r'fx_collapse_shelf_buttons\.collapse_group\s*=\s*' + re.escape(group) + r'(?:\s|$)')

    for btn, btnCommandString in iterShelfButtonCommands(shelf):
        if groupRe.search(btnCommandString):
            m.shelfButton(btn, e=True, visible=state)

        for match in TOGGLE_RE.finditer(btnCommandString):
            if match.groups() == (shelf, group):
                image = IMAGE_OPENED if state else IMAGE_CLOSED
                m.shelfButton(btn, e=True, image=image, image1=image)
                break


def initCollapse():
    if not getShelfTopLevel():
        return

    # need to activate each tab. if you dont you'll get an empty array of buttons if you query them
    cycleThroughShelves()

    toggles = set()
    for shelf in getShelves():
        for _, btnCommandString in iterShelfButtonCommands(shelf):
            for match in TOGGLE_RE.finditer(btnCommandString):
                toggles.add(match.groups())

    for shelf, group in sorted(toggles):
        setGroupState(shelf, group, getSavedState(shelf, group))


def iterShelfButtonCommands(shelf):
    """Yields (button, command string) for each shelf button on the shelf, skipping separators and other controls."""
    for btn in m.shelfLayout(shelf, query=True, childArray=True, fullPathName=True) or []:
        try:
            btnCommandString = m.shelfButton(btn, q=True, command=True)
        except RuntimeError:
            continue
        if btnCommandString:
            yield btn, btnCommandString


def getShelves():
    shelfTopLevel = getShelfTopLevel()
    if not shelfTopLevel:
        return []
    return m.tabLayout(shelfTopLevel, q=True, childArray=True) or []


def cycleThroughShelves():
    shelfTopLevel = getShelfTopLevel()
    currentTabIndex = m.shelfTabLayout(shelfTopLevel, q=True, selectTabIndex=True)

    shelves = getShelves()
    for i in range(1, len(shelves) + 1):
        m.shelfTabLayout(shelfTopLevel, e=True, selectTabIndex=i)
    if shelves:
        m.shelfTabLayout(shelfTopLevel, e=True, selectTabIndex=currentTabIndex)


def getShelfTopLevel():
    shelfTopLevel = mel.eval('global string $gShelfTopLevel; $temp = $gShelfTopLevel')
    if shelfTopLevel and m.shelfTabLayout(shelfTopLevel, exists=True):
        return shelfTopLevel
    return None


def getOptVarName(shelf, group):
    return OPT_VAR_PREFIX + shelf + '_' + group


def getSavedState(shelf, group):
    optVarName = getOptVarName(shelf, group)
    if not m.optionVar(exists=optVarName):
        m.optionVar(intValue=(optVarName, 1))
    return m.optionVar(q=optVarName)


def saveState(shelf, group, state):
    m.optionVar(intValue=(getOptVarName(shelf, group), state))
