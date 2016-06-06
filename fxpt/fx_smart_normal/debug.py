import maya.cmds as m


def locatorByWorldPoint(point, name='dbgLocator'):
    m.spaceLocator(
        absolute=True,
        position=list(point)[:3],
        name=name,
    )
