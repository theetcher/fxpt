from maya.mel import eval as meval

from fxpt.fx_utils import message_box


class CommandDescBase(object):
    def __init__(self, name):
        """
        :type name: str
        """
        self.name = name
        self.run = ''
        self.annotation = ''

    def execute(self):
        raise NotImplementedError('Call to abstract method')

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
        return '{} -> name:{}; run:{}; annotation:{}'.format(type(self).__name__, self.name, self.run, self.annotation)


class CommandDescPython(CommandDescBase):
    def execute(self):
        try:
            exec self.run
        except StandardError:
            message_box.exception('Error during Python command execution')
            raise


class CommandDescMel(CommandDescBase):
    def execute(self):
        try:
            meval(self.run)
        except StandardError:
            message_box.exception('Error during MEL command execution')
            raise
