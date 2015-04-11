from maya import cmds as m
from fxpt.fx_utils.utilsMaya import getShape, getParent


class TransformHandle(object):
    def __init__(self, transform=None, shape=None):
        if (transform is not None) and (m.objExists(transform)):
            self.transform = transform
            self.shape = getShape(transform)
        elif (shape is not None) and (m.objExists(shape)):
            self.transform = getParent(shape)
            self.shape = shape
        else:
            self.transform = None
            self.shape = None

    def __str__(self):
        return 'transform={}, shape={}'.format(self.transform, self.shape)

    def getChildren(self, allDescendants=False, typ=None):
        if typ:
            return sorted(
                m.listRelatives(
                    self.transform,
                    children=True,
                    allDescendents=allDescendants,
                    fullPath=True,
                    typ=typ
                ) or [])
        else:
            return sorted(
                m.listRelatives(
                    self.transform,
                    children=True,
                    allDescendents=allDescendants,
                    fullPath=True
                ) or [])

    def exists(self):
        return (self.transform is not None) and (m.objExists(self.transform))


