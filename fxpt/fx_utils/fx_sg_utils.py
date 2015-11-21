import maya.cmds as m
from maya.mel import eval as meval


# next() is used to find "first occurence of <some condition>" in generator comprehension


def getPolyShadingGroup(polygon):
    shape = m.listRelatives(polygon, parent=True, f=True)[0]
    shadingEngines = set(m.listConnections(shape, source=False, type='shadingEngine') or [])
    # either polygon or shape must be a member of that particular shading engine.
    return next((sg for sg in shadingEngines if m.sets(polygon, isMember=sg)), None) or \
        next((sg for sg in shadingEngines if m.sets(shape, isMember=sg)), None)


def getWorkingData():
    initialSelection = m.ls(sl=True, l=True)

    if not m.ls(sl=True):
        raise RuntimeError('Select mesh or polygon.')

    meval('PolySelectConvert 1')
    polySelection = m.ls(sl=True, l=True, fl=True)

    polygon = next((comp for comp in polySelection if '.f[' in comp), None)

    if not polygon:
        m.select(initialSelection, r=True)
        raise RuntimeError('Select mesh or polygon.')

    sg = getPolyShadingGroup(polygon)

    if not sg:
        m.select(initialSelection, r=True)
        raise RuntimeError('Cannot find shading group on polygon {}.'.format(polygon))

    return sg, polygon, initialSelection


def selectAllShadedByPolygon():
    """
    Selects all nodes/components shaded with the same shading group as selected polygon
    """
    m.select(getWorkingData()[0], r=True)


def selectNeighborsShadedByPolygon():
    """
    Selects all components within current object shaded with the same shading group as selected polygon
    """
    sg, polygon, _ = getWorkingData()

    allMembers = m.ls(m.sets(sg, q=True), l=True)
    shape = m.listRelatives(polygon, parent=True, f=True)[0]
    transform = m.listRelatives(shape, parent=True, f=True)[0]
    m.select([member for member in allMembers if transform in member], r=True)


def duplicateShadingNetworkOnPolygons():
    """
    Get shading network assigned to first polygon in selection, duplicate it and assign result to selection
    """
    sg, _, initialSelection = getWorkingData()

    newSg = m.duplicate(sg, upstreamNodes=True)
    m.sets(initialSelection, e=True, forceElement=newSg[0])
    m.select(initialSelection, r=True)


def showPolygonShaderAttributes():
    """
    Open Attribute Editor of polygon shader
    """
    sg, _, initialSelection = getWorkingData()

    shaderConnection = m.connectionInfo(sg + '.surfaceShader', sourceFromDestination=True) or \
        m.connectionInfo(sg + '.miMaterialShader', sourceFromDestination=True)
    if not shaderConnection:
        raise RuntimeError('Cannot find shader of {}.'.format(sg))

    shader = shaderConnection.split('.')[0]
    m.select(initialSelection, r=True)  # need in case of object (not component) selection to remove highlight
    m.select(shader, r=True)
    meval('showEditor {}'.format(shader))
