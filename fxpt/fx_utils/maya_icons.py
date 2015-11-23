import os
import re

import maya.cmds as m

WINDOW_NAME = 'maya_icons_window'
ICON_WIDTH = 34


def run():

    fileMaskPattern = re.compile(r'^.*\.(?:(?:png)|(?:xpm))$', re.IGNORECASE)
    images = set()

    for path in [p.strip() for p in os.environ['XBMLANGPATH'].split(';')]:
        if not os.path.exists(path):
            continue
        dirContents = os.listdir(path)
        if not dirContents:
            continue

        for i in [f for f in dirContents if os.path.isfile(os.path.join(path, f))]:
            if fileMaskPattern.match(i):
                images.add(i)

    allImages = sorted([str(s) for s in set(m.resourceManager(nf='*.png')) | images], key=str.lower)

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
        numberOfColumns=20,
        columnWidth=[
            (1, ICON_WIDTH),
            (2, ICON_WIDTH),
            (3, ICON_WIDTH),
            (4, ICON_WIDTH),
            (5, ICON_WIDTH),
            (6, ICON_WIDTH),
            (7, ICON_WIDTH),
            (8, ICON_WIDTH),
            (9, ICON_WIDTH),
            (10, ICON_WIDTH),
            (11, ICON_WIDTH),
            (12, ICON_WIDTH),
            (13, ICON_WIDTH),
            (14, ICON_WIDTH),
            (15, ICON_WIDTH),
            (16, ICON_WIDTH),
            (17, ICON_WIDTH),
            (18, ICON_WIDTH),
            (19, ICON_WIDTH),
            (20, ICON_WIDTH),
        ]
    )

    for image in allImages:
        cmd = 'print("{}")'.format(image)
        try:
            m.symbolButton(image=image, ann=image, c=cmd, w=35, h=35)
        except StandardError:
            pass

    m.window(
        WINDOW_NAME,
        e=True,
        wh=[712, 656]
    )
    m.showWindow(WINDOW_NAME)

