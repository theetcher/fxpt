import random

import maya.cmds as m

FILENAMES = [
    '',
    '%FXPT_LOCATION%/src/dirA/testTex_exit.png',
    '%INVALID_ENV_VAR%/fxpt/fx_texture_manager/icons/copy.png',
    '//BEAST/D$/__testTextureManager__/src/dirB/dirB1/retarget.png',
    'C:/__testTextureManagerExternal__/AAA/testTex_exit.png',
    'C:/__testTextureManager__/src/dirB/dirB1/copy.png',
    'C:/__testTextureManager__/src/dirB/dirB1/retarget.png',
    'some/path/tex.png',
    'sourceimages/testTex_exit.png',
    ]


CUBE_SPACING = 2


def createMayaNetwork(filename):
    lambert = m.shadingNode('lambert', asShader=True)
    sg = m.sets(renderable=True, noSurfaceShader=True, empty=True, name=lambert + 'SG')
    m.connectAttr(lambert + '.outColor', sg + '.surfaceShader', force=True)

    fileNode = m.shadingNode('file', asTexture=True)
    placement = m.shadingNode('place2dTexture', asUtility=True)
    m.connectAttr(placement + '.coverage', fileNode + '.coverage', force=True)
    m.connectAttr(placement + '.translateFrame', fileNode + '.translateFrame', force=True)
    m.connectAttr(placement + '.rotateFrame', fileNode + '.rotateFrame', force=True)
    m.connectAttr(placement + '.mirrorU', fileNode + '.mirrorU', force=True)
    m.connectAttr(placement + '.mirrorV', fileNode + '.mirrorV', force=True)
    m.connectAttr(placement + '.stagger', fileNode + '.stagger', force=True)
    m.connectAttr(placement + '.wrapU', fileNode + '.wrapU', force=True)
    m.connectAttr(placement + '.wrapV', fileNode + '.wrapV', force=True)
    m.connectAttr(placement + '.repeatUV', fileNode + '.repeatUV', force=True)
    m.connectAttr(placement + '.offset', fileNode + '.offset', force=True)
    m.connectAttr(placement + '.rotateUV', fileNode + '.rotateUV', force=True)
    m.connectAttr(placement + '.noiseUV', fileNode + '.noiseUV', force=True)
    m.connectAttr(placement + '.vertexUvOne', fileNode + '.vertexUvOne', force=True)
    m.connectAttr(placement + '.vertexUvTwo', fileNode + '.vertexUvTwo', force=True)
    m.connectAttr(placement + '.vertexUvThree', fileNode + '.vertexUvThree', force=True)
    m.connectAttr(placement + '.vertexCameraOne', fileNode + '.vertexCameraOne', force=True)
    m.connectAttr(placement + '.outUV', fileNode + '.uv', force=True)
    m.connectAttr(placement + '.outUvFilterSize', fileNode + '.uvFilterSize', force=True)

    m.connectAttr(fileNode + '.outColor', lambert + '.color', force=True)

    m.setAttr(fileNode + '.fileTextureName', filename, typ='string')

    return sg


def createMRNetwork(filename):
    miaMaterial = m.shadingNode('mia_material_x', asShader=True)
    sg = m.sets(renderable=True, noSurfaceShader=True, empty=True, name=miaMaterial + 'SG')

    m.connectAttr(miaMaterial + '.message', sg + '.miMaterialShader', force=True)
    m.connectAttr(miaMaterial + '.message', sg + '.miPhotonShader', force=True)
    m.connectAttr(miaMaterial + '.message', sg + '.miShadowShader', force=True)

    texLookup = m.shadingNode('mib_texture_lookup', asTexture=True)
    mrTex = m.shadingNode('mentalrayTexture', asTexture=True)

    m.connectAttr(mrTex + '.message', texLookup + '.tex', force=True)
    m.connectAttr(texLookup + '.outValue', miaMaterial + '.diffuse', force=True)
    m.connectAttr(texLookup + '.outValueA', miaMaterial + '.diffuseA', force=True)

    m.setAttr(mrTex + '.fileTextureName', filename, typ='string')

    return sg


shadingNetworkConstructors = [
    createMayaNetwork,
    # createMRNetwork
]


def createCube(x, z):
    cube = m.polyCube(ch=0)[0]
    m.move(x, 0, z, cube, absolute=True)
    return cube


def assignRandomShadingNetwork(faces):
    filename = random.choice(FILENAMES)
    networkConstructor = random.choice(shadingNetworkConstructors)
    sg = networkConstructor(filename)
    m.sets(faces, e=True, forceElement=sg)


def run(xCount, zCount):
    for x in range(xCount):
        for z in range(zCount):
            cube = createCube(x * CUBE_SPACING, z * CUBE_SPACING)

            assignRandomShadingNetwork(cube + '.f[0:2]')
            assignRandomShadingNetwork(cube + '.f[3:5]')
