import maya.cmds as m


def copy():
    polygons = m.ls(m.polyListComponentConversion(tf=True), fl=True, l=True)
    if polygons:
        m.polyClipboard(polygons[0], copy=True, shader=True, uv=True, color=True)


def paste(shader, uv, color):
    #try because of error when selection is empty. mel command handles it without error.
    try:
        m.polyClipboard(paste=True, shader=shader, uv=uv, color=color)
    except:
        pass
