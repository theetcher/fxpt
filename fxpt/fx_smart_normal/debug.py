import maya.cmds as m


def locatorByWorldPoint(point, name='dbgLocator'):
    m.spaceLocator(
        absolute=True,
        position=list(point)[:3],
        name=name,
    )


def dbgPrint(s, on=True):
    if not on:
        return
    print s


def dbgPrintList(l, on=True):
    if not on:
        return
    if not l:
        print []
    else:
        for i, x in enumerate(l):
            print '#{}: {}'.format(i, str(x))


def dbgSelectComps(mesh, polygonIdxs):
    m.select(cl=True)
    for i in polygonIdxs:
        m.select(mesh + '[{}]'.format(i), add=True)
