# fx_collapse_shelf_buttons.collapse_group = group_name
# // fx_collapse_shelf_buttons.collapse_group = group_name

import re

import maya.mel as mel
import maya.cmds as m

import pymel.core as pm

OPT_VAR_PREFIX = 'fx_collapse_shelf_buttons_'


def toggle(shelf, group):
    state = toggleState(getSavedState(shelf, group))
    setGroupState(shelf, group, state)
    saveState(shelf, group, state)


def toggleState(state):
    return 1 if state == 0 else 0


def setGroupState(shelf, group, state):
    shelves = getShelves()
    assert shelf in shelves, 'Cannot find shelf "' + shelf + '".'

    shelfButtons = m.shelfLayout(shelf, query=True, childArray=True, fullPathName=True)
    for btn in shelfButtons:
        btnCommandString = m.shelfButton(btn, q=True, command=True)

        match = re.search(r'.*fx_collapse_shelf_buttons\.collapse_group\s*=\s*' + re.escape(group) + r'\s+.*',
                          btnCommandString)
        if match:
            m.shelfButton(btn, e=True, visible=state)

        pattern = r"fx_collapse_shelf_buttons.toggle\(\'" + re.escape(shelf) + r"\'\,\s*\'" + re.escape(group) + r"\'\)"
        match = re.search(pattern, btnCommandString)
        if match:
            image = 'collapseBarOpened.png' if state else 'collapseBarClosed.png'
            m.shelfButton(btn, e=True, image=image, image1=image)


def initCollapse():
    # need to activate each tab. if you dont you'll get an empty array of buttons if you query them
    cycleThroughShelves()

    for shelf in getShelves():
        shelfButtons = m.shelfLayout(shelf, query=True, childArray=True, fullPathName=True)
        if shelfButtons is not None:
            for btn in shelfButtons:
                btnCommandString = m.shelfButton(btn, q=True, command=True)
                match = re.search(r"fx_collapse_shelf_buttons.toggle\(\'(.*)\'\,\s*\'(.*)\'\)", btnCommandString)
                if match:
                    shelf, group = match.group(1), match.group(2)
                    state = getSavedState(shelf, group)
                    setGroupState(shelf, group, state)


def getShelves():
    return m.tabLayout(getShelfTopLevel(), q=True, childArray=True)


def cycleThroughShelves():
    shelfTopLevel = getShelfTopLevel()
    currentTabIndex = m.shelfTabLayout(shelfTopLevel, q=True, selectTabIndex=True)

    shelves = getShelves()
    for i in range(1, len(shelves) + 1):
        m.shelfTabLayout(shelfTopLevel, e=True, selectTabIndex=i)
    m.shelfTabLayout(shelfTopLevel, e=True, selectTabIndex=currentTabIndex)


def getShelfTopLevel():
    return mel.eval('global string $gShelfTopLevel; $temp = $gShelfTopLevel')


def getSavedState(shelf, group):
    optVarName = OPT_VAR_PREFIX + shelf + '_' + group
    optVars = pm.env.optionVars
    if optVarName not in optVars:
        optVars[optVarName] = 1
    return optVars[optVarName]


def saveState(shelf, group, state):
    optVarName = OPT_VAR_PREFIX + shelf + '_' + group
    optVars = pm.env.optionVars
    optVars[optVarName] = state
