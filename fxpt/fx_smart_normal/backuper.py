import maya.cmds as m


class Backuper(object):
    """
    :type mesh: str
    :type transform: str
    :type origMeshCopy: str

    :type vcDisplay: bool
    :type vcColorChannel: str
    :type normalDisplay: tuple[bool]
    """
    def __init__(self, mesh, transform):
        self.mesh = mesh
        self.transform = transform
        self.origMeshCopy = None

        self.vcDisplay = None
        self.vcColorChannel = None
        self.normalDisplay = None

        self.backupAll()

    def backupAll(self):
        self.backupDisplay()
        self.backupNormals()

    def backupDisplay(self):
        self.vcDisplay = m.polyOptions(q=True, colorShadedDisplay=True)[0]
        self.vcColorChannel = m.polyOptions(q=True, colorMaterialChannel=True)[0]

        self.normalDisplay = (
            m.polyOptions(self.mesh, q=True, displayNormal=True)[0],
            m.polyOptions(self.mesh, q=True, facet=True)[0],
            m.polyOptions(self.mesh, q=True, point=True)[0],
            m.polyOptions(self.mesh, q=True, pointFacet=True)[0],
        )

    def backupNormals(self):
        copyTr = m.duplicate(self.mesh)
        copyMesh = m.listRelatives(copyTr, fullPath=True, shapes=True, typ='mesh')
        self.origMeshCopy = m.parent(copyMesh, self.transform, shape=True, add=True)[0]
        m.setAttr(self.origMeshCopy + '.intermediateObject', True)
        m.delete(copyTr)

    def restoreAll(self):
        self.restoreDisplay()
        self.restoreNormals()

    def restoreDisplay(self):
        m.polyOptions(self.mesh, colorShadedDisplay=self.vcDisplay)
        m.polyOptions(self.mesh, colorMaterialChannel=self.vcColorChannel)

        m.polyOptions(self.mesh, displayNormal=self.normalDisplay[0], facet=self.normalDisplay[1])
        m.polyOptions(self.mesh, displayNormal=self.normalDisplay[0], point=self.normalDisplay[2])
        m.polyOptions(self.mesh, displayNormal=self.normalDisplay[0], pointFacet=self.normalDisplay[3])

    def restoreNormals(self):
        m.setAttr(self.origMeshCopy + '.intermediateObject', False)
        m.delete(self.mesh)

    def deleteBackup(self):
        m.delete(self.origMeshCopy)
