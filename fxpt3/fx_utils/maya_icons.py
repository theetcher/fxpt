import os
import re

import maya.cmds as m

WINDOW_NAME = 'maya_icons_window'
ICON_WIDTH = 34
COLUMNS = 20


def printName(name):
    print(name)


def run():

    fileMaskPattern = re.compile(r'^.*\.(?:(?:png)|(?:xpm))$', re.IGNORECASE)
    images = set()

    for path in [p.strip() for p in os.environ.get('XBMLANGPATH', '').split(os.pathsep)]:
        if not path or not os.path.isdir(path):
            continue

        for i in os.listdir(path):
            if fileMaskPattern.match(i) and os.path.isfile(os.path.join(path, i)):
                images.add(i)

    allImages = sorted(set(m.resourceManager(nf='*.png') or []) | images, key=str.lower)

    if m.window(WINDOW_NAME, exists=True):
        m.deleteUI(WINDOW_NAME)

    m.window(
        WINDOW_NAME,
        t='{} maya icons'.format(len(allImages)),
        w=700,
        h=650
    )

    m.scrollLayout()

    m.rowColumnLayout(
        numberOfColumns=COLUMNS,
        columnWidth=[(i, ICON_WIDTH) for i in range(1, COLUMNS + 1)]
    )

    for image in allImages:
        try:
            m.symbolButton(image=image, ann=image, c=lambda *_, name=image: printName(name), w=35, h=35)
        except RuntimeError:
            pass

    m.window(
        WINDOW_NAME,
        e=True,
        wh=[712, 656]
    )
    m.showWindow(WINDOW_NAME)
