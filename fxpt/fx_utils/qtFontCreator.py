from PySide import QtGui


class QtFontCreator(object):

    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
        self.qFont = self.qFontFromFile()

    def qFontFromFile(self):
        fontID = QtGui.QFontDatabase.addApplicationFont(self.filename)
        fontFamily = QtGui.QFontDatabase.applicationFontFamilies(fontID)[0]
        return QtGui.QFont(fontFamily, self.size)

    def getQFont(self):
        return self.qFont

    def getLetterSize(self, letter):
        return QtGui.QFontMetrics(self.qFont).width(letter)