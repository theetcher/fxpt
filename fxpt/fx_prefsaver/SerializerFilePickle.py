import os

# noinspection PyBroadException
try:
    import cPickle as pickle
except:
    import pickle

from SerializerBase import SerializerBase

from com import message


class SerializerFilePickle(SerializerBase):

    def __init__(self, filename):
        super(SerializerFilePickle, self).__init__()
        self.filename = filename

    def save(self, obj):
        try:
            f = open(self.filename, 'wb')
            try:
                pickle.dump(obj, f, -1)
            finally:
                f.close()
        except IOError as e:
            message('Error writing file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise
        except Exception as e:
            message('Unknown error occurred while saving the file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise

    def load(self):
        if not os.path.exists(self.filename):
            return {}

        try:
            f = open(self.filename, 'rb')
            try:
                obj = pickle.load(f)
            finally:
                f.close()
        except IOError as e:
            message('Error reading file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise
        except Exception as e:
            message('Unknown error occurred while reading a file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise

        return obj


