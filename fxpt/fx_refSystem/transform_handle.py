from maya import cmds as m
from fxpt.fx_utils.utilsMaya import getShape, getParent, parentAPI


# noinspection PyAttributeOutsideInit
class TransformHandle(object):
    def __init__(self, transform=None, shape=None):
        self.initHandle(transform, shape)

    def __str__(self):
        return 'transform={}, shape={}'.format(self.transform, self.shape)

    def initHandle(self, transform=None, shape=None):
        if (transform is not None) and (m.objExists(transform)):
            self.transform = transform
            self.shape = getShape(transform)
        elif (shape is not None) and (m.objExists(shape)):
            self.transform = getParent(shape)
            self.shape = shape
        else:
            self.transform = None
            self.shape = None

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

    def getParents(self, typ=None):
        if typ:
            return sorted(
                m.listRelatives(
                    self.transform,
                    parent=True,
                    fullPath=True,
                    typ=typ
                ) or [])
        else:
            return sorted(
                m.listRelatives(
                    self.transform,
                    parent=True,
                    fullPath=True
                ) or [])

    def parent(self, newParent, absolute=True):
        pass

    def exists(self):
        return (self.transform is not None) and (m.objExists(self.transform))


