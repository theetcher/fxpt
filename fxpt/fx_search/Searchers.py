import re
import os
from PySide import QtCore, QtGui

from Com import *

from fxpt.fx_refSystem.ref_handle import ATTR_REF_FILENAME
from fxpt.fx_utils.utilsMaya import getParent


class NodeInfo(object):

    def __init__(self):
        self.selectionString = None
        self.fullPathName = None
        self.shortName = None


class SearchDesc(object):

    def __init__(self):
        self.searchString = None
        self.caseSensitive = None
        self.regex = None
        self.selectFound = None
        self.includeShapes = None
        self.searchSelected = None


class SearcherBase(object):

    def __init__(self, name):
        self.name = name
        self.active = False
        self.searchDesc = None
        self.model = QtGui.QStandardItemModel()
        self.initModel()

    def search(self, sd):
        if not self.getActive():
            return
        self.initModel()
        self.searchDesc = sd
        searchData = self.gatherSearchData()
        matchedData = self.doSearch(searchData)
        modelData = self.prepareModelData(matchedData)
        self.fillModel(modelData)

    def getName(self):
        return self.name

    def getModel(self):
        return self.model

    def setActive(self, state):
        self.active = state

    def getActive(self):
        return self.active

    def hasResult(self):
        return bool(self.model.rowCount())

    def reset(self):
        self.model.clear()

    def filterShapes(self, nodes):
        if self.searchDesc.includeShapes:
            return nodes
        else:
            return [x for x in nodes if not isShape(x)]

    def getRegexpObject(self):
        searchPattern = self.searchDesc.searchString
        if not self.searchDesc.regex:
            searchPattern = re.escape(searchPattern)
            if searchPattern.startswith('\?'):
                searchPattern = '^' + searchPattern
            if searchPattern.endswith('\?'):
                searchPattern += '$'
            searchPattern = re.sub(r'\\\?', r'.', searchPattern)
            searchPattern = re.sub(r'\\\*', r'.*', searchPattern)

        if self.searchDesc.caseSensitive:
            regexp = re.compile(searchPattern)
        else:
            regexp = re.compile(searchPattern, flags=re.IGNORECASE)

        return regexp

    def doSearch(self, searchData):
        regexp = self.getRegexpObject()
        return [item for item in searchData if regexp.search(item[1])]

    def initModel(self):
        columnNames = self.getColumnNames()
        self.model.clear()
        self.model.setRowCount(0)
        self.model.setColumnCount(len(columnNames))
        for i, col in enumerate(columnNames):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, col, QtCore.Qt.DisplayRole)

    def fillModel(self, modelData):
        if not modelData:
            return

        itemsNum = len(modelData)
        colNum = len(modelData[0]) - 1

        self.model.insertRows(0, itemsNum)

        for i, modelRowDataItem in enumerate(modelData):
            for col in range(colNum):
                modelIndex = self.model.index(i, col)
                self.model.setData(modelIndex, modelRowDataItem[col])
            modelIndex = self.model.index(i, 0)
            self.model.setData(modelIndex, modelRowDataItem[-1], QtCore.Qt.UserRole)

    def getColumnNames(self):
        raise NotImplementedError("Call to abstract method.")

    def gatherSearchData(self):
        raise NotImplementedError("Call to abstract method.")

    def prepareModelData(self, matchedData):
        raise NotImplementedError("Call to abstract method.")


class SearcherSimpleBase(SearcherBase):

    def __init__(self, name):
        super(SearcherSimpleBase, self).__init__(name)

    def getColumnNames(self):
        return [
            'Name',
            'Type',
            'Path'
        ]

    def getTargetNodes(self):
        raise NotImplementedError("Call to abstract method.")

    def gatherSearchData(self):
        # return [(fullPathName, searchField), (fullPathName, searchField), ...]
        allNodes = self.getTargetNodes()
        searchData = [(x, shortNameOf(x)) for x in self.filterShapes(allNodes)]
        return searchData

    def prepareModelData(self, matchedData):
        # input [(fullPathName, searchField), ....]
        # return [(shortName, type, path, nodeInfo), ...]
        modelData = []
        for matchedItem in matchedData:
            fullPathName = matchedItem[0]
            shortName = matchedItem[1]
            path = pathOf(fullPathName)

            typ = getNodeTypeString(fullPathName)

            ni = NodeInfo()
            ni.selectionString = [fullPathName]
            ni.fullPathName = fullPathName
            ni.shortName = shortName

            modelData.append((shortName, typ, path, ni))

        return modelData


class SearcherNodes(SearcherSimpleBase):

    def __init__(self, name):
        super(SearcherNodes, self).__init__(name)

    def getTargetNodes(self):
        if self.searchDesc.searchSelected:
            allNodes = m.ls(sl=True, l=True)
        else:
            allNodes = m.ls(l=True)
        return allNodes


class SearcherDagNodes(SearcherSimpleBase):

    def __init__(self, name):
        super(SearcherDagNodes, self).__init__(name)

    def getTargetNodes(self):
        if self.searchDesc.searchSelected:
            allNodes = m.ls(sl=True, l=True, dag=True)
        else:
            allNodes = m.ls(l=True, dag=True)

        return allNodes


class SearcherTransforms(SearcherSimpleBase):

    def __init__(self, name):
        super(SearcherTransforms, self).__init__(name)

    def getTargetNodes(self):
        if self.searchDesc.searchSelected:
            allNodes = m.ls(sl=True, l=True, transforms=True)
        else:
            allNodes = m.ls(l=True, transforms=True)

        return allNodes


class SearcherType(SearcherBase):

    def __init__(self, name):
        super(SearcherType, self).__init__(name)

    def getColumnNames(self):
        return [
            'Node Name',
            'Node Type',
            'Path'
        ]

    def gatherSearchData(self):
        # return [(fullPathName, searchField), (fullPathName, searchField), ...]
        if self.searchDesc.searchSelected:
            nodes = m.ls(sl=True, l=True)
        else:
            nodes = m.ls(l=True)
        return [(x, typeOf(x)) for x in nodes]

    def prepareModelData(self, matchedData):
        # input [(fullPathName, searchField), ....]
        # return [(shortName, type, path, nodeInfo), ...]
        modelData = []
        for matchedItem in matchedData:
            fullPathName = matchedItem[0]
            shortName = shortNameOf(fullPathName)
            path = pathOf(fullPathName)

            typ = getNodeTypeString(fullPathName)

            ni = NodeInfo()
            ni.selectionString = [fullPathName]
            ni.fullPathName = fullPathName
            ni.shortName = shortName

            modelData.append((shortName, typ, path, ni))

        return modelData


class SearcherTexturesBase(SearcherBase):

    def __init__(self, name):
        super(SearcherTexturesBase, self).__init__(name)

    def getColumnNames(self):
        return [
            'Name',
            'Texture',
            'Path'
        ]

    def gatherSearchData(self):
        # return [(fullPathName, searchField), (fullPathName, searchField), ...]

        if self.searchDesc.searchSelected:
            fileNodes = m.ls(sl=True, l=True, typ='file')
        else:
            fileNodes = m.ls(l=True, typ='file')

        searchData = []
        for f in fileNodes:
            filename = m.getAttr(f + '.fileTextureName')
            sFilename = os.path.basename(filename)
            searchData.append((f, sFilename))
        return searchData


class SearcherTextures(SearcherTexturesBase):

    def __init__(self, name):
        super(SearcherTextures, self).__init__(name)

    def prepareModelData(self, matchedData):
        # input [(fullPathName, searchField), ....]
        # return [(fileNodeName, textureShortName, fileNodeTexturePath, nodeInfo), ...]
        modelData = []
        for matchedItem in matchedData:
            fullPathName = matchedItem[0]
            shortName = shortNameOf(fullPathName)

            fileNodeTexturePath = m.getAttr(fullPathName + '.fileTextureName')
            textureShortName = os.path.basename(fileNodeTexturePath)

            ni = NodeInfo()
            ni.selectionString = [fullPathName]
            ni.fullPathName = fullPathName
            ni.shortName = shortName

            modelData.append((shortName, textureShortName, fileNodeTexturePath, ni))

        return modelData


class SearcherTexturedBy(SearcherTexturesBase):

    def __init__(self, name):
        super(SearcherTexturesBase, self).__init__(name)
        self.visitedNodes = set()

    def prepareModelData(self, matchedData):
        # input [(fullPathName, searchField), ....]
        # return [(fileNodeName, textureShortName, fileNodeTexturePath, nodeInfo), ...]
        modelData = []
        for matchedItem in matchedData:
            fullPathName = matchedItem[0]
            shortName = shortNameOf(fullPathName)

            fileNodeTexturePath = m.getAttr(fullPathName + '.fileTextureName')
            textureShortName = os.path.basename(fileNodeTexturePath)

            shadingGroups = self.getShadingGroups(fullPathName)

            selectionStrings = []
            for sg in shadingGroups:
                selectionStrings.extend(m.sets(sg, q=True))

            ni = NodeInfo()
            ni.selectionString = selectionStrings
            ni.fullPathName = fullPathName
            ni.shortName = shortName

            modelData.append((shortName, textureShortName, fileNodeTexturePath, ni))

        return modelData

    def getShadingGroups(self, fileNode):

        self.visitedNodes.clear()
        self.visitedNodes.add(fileNode)

        res = []

        destinations = m.listConnections(fileNode, s=False, d=True)

        if destinations:
            for d in destinations:
                if d in self.visitedNodes:
                    continue
                if typeOf(d) == 'shadingEngine':
                    res.append(d)
                    continue
                res.extend(self.getShadingGroups(d))

        return res


class SearcherFxRefs(SearcherBase):

    def __init__(self, name):
        super(SearcherFxRefs, self).__init__(name)

    # noinspection PyMethodMayBeStatic
    def getRefFilename(self, refLoc):
        return m.getAttr('{}.{}'.format(refLoc, ATTR_REF_FILENAME))

    # noinspection PyMethodMayBeStatic
    def isRefLocator(self, refLoc):
        return m.objExists('{}.{}'.format(refLoc, ATTR_REF_FILENAME))

    def getColumnNames(self):
        return [
            'Exists',
            'Name',
            'Filename',
            'Path'
        ]

    def gatherSearchData(self):
        # return [(fullPathName, searchField), (fullPathName, searchField), ...]
        if self.searchDesc.searchSelected:
            locators = m.ls(sl=True, l=True, dag=True, ap=True, typ='locator')
        else:
            locators = m.ls(l=True, typ='locator')

        res = []
        for loc in locators:
            if self.isRefLocator(loc):
                filename = self.getRefFilename(loc)
                shortName = os.path.splitext(os.path.basename(filename))[0]
                res.append((loc, shortName))

        return res

    def prepareModelData(self, matchedData):
        # input [(fullPathName, searchField), ....]
        # return [(exists, shortName, filename, mayaPath, nodeInfo), ...]
        modelData = []

        for fullPathName, shortName in matchedData:

            filename = self.getRefFilename(fullPathName)
            exists = 'Yes' if os.path.exists(os.path.expandvars(filename)) else 'No'
            mayaPath = getParent(fullPathName)

            ni = NodeInfo()
            ni.selectionString = [mayaPath]
            ni.fullPathName = mayaPath
            ni.shortName = shortName

            modelData.append((exists, shortName, filename, mayaPath, ni))

        print modelData

        return modelData
