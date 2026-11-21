import maya.cmds as m


def copy():
    polygons = m.ls(m.polyListComponentConversion(tf=True) or [], fl=True, l=True)
    if polygons:
        m.polyClipboard(polygons[0], copy=True, shader=True, uv=True, color=True)


def paste(shader, uv, color):
    # polyClipboard raises when the selection is empty, the mel command handles it without error.
    if not m.ls(sl=True):
        return
    try:
        m.polyClipboard(paste=True, shader=shader, uv=uv, color=color)
    except RuntimeError:
        pass
