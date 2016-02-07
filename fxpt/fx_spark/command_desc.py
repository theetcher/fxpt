from maya.mel import eval as meval


class CommandDesc(object):
    def __init__(self, name):
        """
        :type name: str
        """
        self.name = name
        self.run = ''
        self.annotation = ''

    def execute(self):
        meval(self.run)

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __le__(self, other):
        return self.name <= other.name

    def __eq__(self, other):
        return self.name == other.name

    def __ge__(self, other):
        return self.name >= other.name

    def __gt__(self, other):
        return self.name > other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'name:{}; run:{}; annotation:{}'.format(self.name, self.run, self.annotation)
