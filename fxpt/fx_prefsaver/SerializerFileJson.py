import os

import json

from SerializerBase import SerializerBase

from com import message


class SerializerFileJson(SerializerBase):

    def __init__(self, filename):
        super(SerializerFileJson, self).__init__()
        self.filename = filename

    def save(self, obj):
        try:
            f = open(self.filename, 'wb')
            try:
                json.dump(obj, f, sort_keys=True, indent=4, separators=(',', ': '))
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
                obj = json.load(f)
            finally:
                f.close()
        except IOError as e:
            message('Error reading file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise
        except Exception as e:
            message('Unknown error occurred while reading a file. Filename: {}.\nAdditional exception info:\n{}'.format(self.filename, str(e)))
            raise

        return obj


