from PySide import QtGui, QtCore

from . import search_line_edit, results_list_widget, searcher, cfg


class ClosePopupFilter(QtCore.QObject):

    # noinspection PyMethodOverriding
    def eventFilter(self, target, event):
        eventType = event.type()
        if eventType == QtCore.QEvent.WindowDeactivate:
            target.close()
        elif eventType == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape:
            target.close()
        return False


# noinspection PyAttributeOutsideInit
class SparkUI(QtGui.QWidget):

    def __init__(self, parent):
        """
        :type parent: QtGui.QWidget
        """
        super(SparkUI, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.popupFilter = ClosePopupFilter()
        self.installEventFilter(self.popupFilter)

        self.mayaWindow = parent

        self.createUI()

        self.searcher = searcher.Searcher()

        self.setStyleSheet(cfg.STYLE_SHEET)
        self.activateWindow()
        self.uiLED_search.setFocus()

        self.onSearchTextChanged()
        self.setAnnotation(cfg.UI_DEFAULT_ANNOTATION)

    def createUI(self):
        self.positionUi()

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        widgetLayout = QtGui.QVBoxLayout()
        widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(widgetLayout)

        mainFrame = QtGui.QFrame()
        widgetLayout.addWidget(mainFrame)

        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(cfg.UI_CONTENTS_MARGIN, 0, cfg.UI_CONTENTS_MARGIN, cfg.UI_CONTENTS_MARGIN)
        mainFrame.setLayout(layout)

        self.uiLBL_annotation = QtGui.QLabel(cfg.UI_DEFAULT_ANNOTATION)
        self.uiLBL_annotation.setFixedHeight(cfg.UI_LABEL_HEIGHT)
        layout.addWidget(self.uiLBL_annotation)

        self.uiLBL_status = QtGui.QLabel(cfg.UI_DEFAULT_STATUS)
        self.uiLBL_status.setFixedHeight(cfg.UI_LABEL_HEIGHT)

        self.uiLED_search = search_line_edit.SearchLineEdit()
        self.uiLED_search.setFixedHeight(cfg.UI_SEARCH_FIELD_HEIGHT)
        self.uiLST_results = results_list_widget.ResultsListWidget()
        self.uiLED_search.setPartner(self.uiLST_results)
        self.uiLST_results.setPartner(self.uiLED_search)

        layout.addWidget(self.uiLED_search)
        layout.addWidget(self.uiLBL_status)
        layout.addWidget(self.uiLST_results)

        layout.addStretch()

        self.uiLED_search.textChanged.connect(self.onSearchTextChanged)
        self.uiLST_results.itemActivated.connect(self.onItemActivated)
        self.uiLST_results.currentRowChanged.connect(self.onResultSelectionChanged)

    def positionUi(self):
        self.setFixedWidth(cfg.UI_FRAME_WIDTH)

        geom = self.mayaWindow.geometry()
        mayaWinCenterLeft = geom.left() + geom.width() / 2
        mayaWinCenterTop = geom.top() + geom.height() / 2
        self.move(mayaWinCenterLeft - cfg.UI_FRAME_WIDTH / 2, mayaWinCenterTop + cfg.UI_FRAME_CENTER_OFFSET)

    def getSearchText(self):
        return self.uiLED_search.text().strip()

    def onSearchTextChanged(self):
        results = self.searcher.search(self.getSearchText())
        self.displayResults(results)

    def onItemActivated(self, item):
        if item:
            self.close()
            item.desc.execute()
            self.searcher.commandExecuted(item.desc)

    def onResultSelectionChanged(self, i):
        if i is not None and i > -1:
            self.setAnnotation(self.uiLST_results.item(i).desc.annotation)
        else:
            self.setAnnotation(cfg.UI_DEFAULT_ANNOTATION)

    def setAnnotation(self, text):
        self.uiLBL_annotation.setText(text)

    def setStatus(self, text):
        self.uiLBL_status.setText(text)

    def displayResults(self, results):
        resultsNum = len(results)

        if self.getSearchText():
            self.setStatus('{} match{}:'.format(resultsNum, '' if resultsNum == 1 else 'es'))
        else:
            self.setStatus(cfg.UI_DEFAULT_STATUS)

        self.uiLST_results.clear()

        for r in sorted(results, key=lambda i: i.name.lower()):
            item = self.createResultItem(r)
            self.uiLST_results.addItem(item)

        if resultsNum:
            self.uiLST_results.setCurrentRow(0)

        self.updateUiGeom()

    def updateUiGeom(self):
        if not self.uiLST_results.count():
            self.uiLST_results.setVisible(False)
            listHeight = 0
        else:
            self.uiLST_results.setVisible(True)
            maxHeight = self.uiLST_results.count() * cfg.UI_ITEM_SIZE + cfg.UI_LIST_SIZE_BOTTOM_MARGIN
            listHeight = min(maxHeight, cfg.UI_MAX_RESULTS_HEIGHT)
            self.uiLST_results.setFixedHeight(listHeight)

        margin = cfg.UI_CONTENTS_MARGIN
        annotationHeight = self.uiLBL_annotation.height()
        ledHeight = self.uiLED_search.height()
        statusHeight = self.uiLBL_status.height()

        height = \
            margin + \
            annotationHeight + \
            ledHeight + \
            statusHeight + \
            listHeight + \
            margin

        self.setFixedHeight(height)

    # noinspection PyMethodMayBeStatic
    def createResultItem(self, desc):
        item = QtGui.QListWidgetItem(desc.name)
        item.desc = desc
        sizeHint = item.sizeHint()
        sizeHint.setHeight(cfg.UI_ITEM_SIZE)
        item.setSizeHint(sizeHint)
        return item
