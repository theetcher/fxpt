import maya.cmds as m
from maya.mel import eval as meval


# next() is used to find "first occurence of <some condition>" in generator comprehension

SHADER_ATTRS = ('surfaceShader', 'aiSurfaceShader', 'miMaterialShader')


def getPolyShadingGroup(polygon):
    shape = m.listRelatives(polygon, parent=True, f=True)[0]
    shadingEngines = set(m.listConnections(shape, source=False, type='shadingEngine') or [])
    # either polygon or shape must be a member of that particular shading engine.
    return next((sg for sg in shadingEngines if m.sets(polygon, isMember=sg)), None) or \
        next((sg for sg in shadingEngines if m.sets(shape, isMember=sg)), None)


def getWorkingData():
    initialSelection = m.ls(sl=True, l=True)

    if not initialSelection:
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


def isMemberOf(member, node):
    """
    True if member is node itself or a component of it
    """
    return member == node or member.startswith(node + '.')


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

    allMembers = m.ls(m.sets(sg, q=True) or [], l=True)
    shape = m.listRelatives(polygon, parent=True, f=True)[0]
    transform = m.listRelatives(shape, parent=True, f=True)[0]
    m.select([member for member in allMembers if isMemberOf(member, shape) or isMemberOf(member, transform)], r=True)


def duplicateShadingNetworkOnPolygons():
    """
    Get shading network assigned to first polygon in selection, duplicate it and assign result to selection
    """
    sg, _, initialSelection = getWorkingData()

    m.undoInfo(openChunk=True)
    try:
        newSg = m.duplicate(sg, upstreamNodes=True)
        m.sets(initialSelection, e=True, forceElement=newSg[0])
        m.select(initialSelection, r=True)
    finally:
        m.undoInfo(closeChunk=True)


def getShader(sg):
    for attr in SHADER_ATTRS:
        if not m.attributeQuery(attr, node=sg, exists=True):
            continue
        connection = m.connectionInfo('{}.{}'.format(sg, attr), sourceFromDestination=True)
        if connection:
            return connection.split('.')[0]
    return None


def showPolygonShaderAttributes():
    """
    Open Attribute Editor of polygon shader
    """
    sg, _, initialSelection = getWorkingData()

    m.select(initialSelection, r=True)  # need in case of object (not component) selection to remove highlight

    shader = getShader(sg)
    if not shader:
        raise RuntimeError('Cannot find shader of {}.'.format(sg))

    m.select(shader, r=True)
    meval('showEditor "{}"'.format(shader))
