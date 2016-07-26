import maya.cmds as m
import maya.api.OpenMaya as om

from fx_utils.watch import watch


DEBUG = False


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
    selList = om.MSelectionList()
    selList.add(m.ls(sl=True, l=True)[0])
    dagPath = selList.getDagPath(0)
    return om.MFnMesh(dagPath)


def colorize(orientations):
    maxLength = max([o.length() for o in orientations])
    colors = []
    for o in orientations:
        colors.append(om.MColor(o / maxLength + om.MVector(1, 1, 0)) * 0.5)
    return colors


def _watch(*args, **kwargs):
    if DEBUG:
        watch(*args, **kwargs)


def generateFlowMap():
    locators = getLocators()
    _watch(locators)

    meshFn = getMeshFn()
    vertices = getVertices(meshFn)
    # _watch(vertices)

    orientations = []
    for iv, v in enumerate(vertices):

        lowSlopeWidth = 50
        bellTopWidth = 4

        weightsNoNorm = [(1 / (1 + abs((l.position - v).length() / lowSlopeWidth) ** bellTopWidth)) * l.orientationLength for l in locators]
        _watch(weightsNoNorm, 'weightsNoNorm')

        normFactor = 1 / sum(weightsNoNorm)
        _watch(normFactor, 'normFactor')

        weights = [w * normFactor for w in weightsNoNorm]
        _watch(weights, 'weights')

        resultOrientation = om.MVector(0, 0, 0)
        for i, l in enumerate(locators):
            resultOrientation = resultOrientation + l.orientation * weights[i]

        # UE4 uses left handed coord system
        orientations.append(om.MVector(-resultOrientation.x, resultOrientation.y, resultOrientation.z))

    _watch(orientations, 'orientations')

    colors = colorize(orientations)

    _watch(colors, 'colors')

    meshFn.setVertexColors(colors, range(len(vertices)))



def run():
    generateFlowMap()
