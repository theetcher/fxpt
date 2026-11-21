import maya.cmds as m
import maya.api.OpenMaya as om

from fxpt3.fx_utils.watch import watch


DEBUG = False

LOW_SLOPE_WIDTH = 50.0
BELL_TOP_WIDTH = 4


def getParent(node):
    parents = m.listRelatives(node, parent=True, fullPath=True)
    if parents:
        return parents[0]
    else:
        return None


class Locator(object):
    # noinspection PyArgumentList
    def __init__(self, path):
        self.transform = path
        selList = om.MSelectionList()
        selList.add(self.transform)
        dagPath = selList.getDagPath(0)
        self.transformFn = om.MFnTransform(dagPath)
        self.position = om.MPoint(self.transformFn.translation(om.MSpace.kWorld))
        self.orientation = om.MVector(0, 1, 0) * om.MMatrix(m.getAttr(self.transform + '.worldMatrix'))
        self.orientationLength = self.orientation.length()
        self.color = None

    def __str__(self):
        return 'Locator: transform={}, position={}, orientation={}, orientationLength={}'.format(self.transform, self.position, self.orientation, self.orientationLength)


def getLocators():
    return [Locator(getParent(x)) for x in m.ls(l=True, visible=True, typ='locator')]


def getVertices(meshFn):
    return [om.MPoint(v) for v in meshFn.getPoints(space=om.MSpace.kWorld)]


def getMeshFn():
    selection = m.ls(sl=True, l=True, objectsOnly=True)
    if not selection:
        return None
    selList = om.MSelectionList()
    selList.add(selection[0])
    dagPath = selList.getDagPath(0)
    try:
        return om.MFnMesh(dagPath)
    except RuntimeError:
        return None


def colorize(orientations):
    maxLength = max([o.length() for o in orientations])
    if maxLength < 1e-12:
        maxLength = 1.0
    colors = []
    for o in orientations:
        c = (o / maxLength + om.MVector(1, 1, 0)) * 0.5
        colors.append(om.MColor([c.x, c.y, c.z]))
    return colors


def _watch(*args, **kwargs):
    if DEBUG:
        watch(*args, **kwargs)


def generateFlowMap():
    meshFn = getMeshFn()
    if meshFn is None:
        m.warning('Select a polygon mesh.')
        return

    locators = getLocators()
    if not locators:
        m.warning('No visible locators in the scene.')
        return
    _watch([str(l) for l in locators], 'locators')

    vertices = getVertices(meshFn)
    if not vertices:
        m.warning('The selected mesh has no vertices.')
        return

    orientations = []
    for v in vertices:

        # weightsNoNorm = [(1 / (1 + abs((l.position - v).length() / LOW_SLOPE_WIDTH) ** BELL_TOP_WIDTH)) * l.orientationLength for l in locators]
        weightsNoNorm = [(1 / (1 + abs((l.position - v).length() / LOW_SLOPE_WIDTH) ** BELL_TOP_WIDTH)) for l in locators]
        _watch(weightsNoNorm, 'weightsNoNorm')

        normFactor = 1 / sum(weightsNoNorm)
        _watch(normFactor, 'normFactor')

        weights = [w * normFactor for w in weightsNoNorm]
        _watch(weights, 'weights')

        resultOrientation = om.MVector(0, 0, 0)
        for i, l in enumerate(locators):
            resultOrientation += l.orientation * weights[i]

        orientations.append(resultOrientation)

    _watch([str(o) for o in orientations], 'orientations')

    colors = colorize(orientations)

    _watch([str(c) for c in colors], 'colors')

    meshFn.setVertexColors(colors, list(range(len(vertices))))


def run():
    generateFlowMap()
