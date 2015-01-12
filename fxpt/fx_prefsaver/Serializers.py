import os
import json

# noinspection PyBroadException
try:
    import cPickle as pickle
except:
    import pickle

# noinspection PyBroadException
try:
    import maya.cmds as m
except:
    m = None

from com import message


class SerializerBase(object):

    def __init__(self):
        pass

    def save(self, obj):
        raise NotImplementedError('Call to abstract method')

    def load(self):
        raise NotImplementedError('Call to abstract method')


class SerializerFileBase(SerializerBase):

    def __init__(self, filename):
        super(SerializerFileBase, self).__init__()
        self.filename = filename

    def save(self, obj):
        try:
            f = open(self.filename, 'wb')
            try:
                self.saveProcedure(obj, f)
            finally:
                f.close()
        except IOError as e:
            message('Error writing file. Filename: {0}.\nAdditional exception info:\n{1}'.format(self.filename, str(e)))
            raise
        except Exception as e:
            message('Error occurred during serialization. Filename: {0}.\nAdditional exception info:\n{1}'.format(self.filename, str(e)))
            raise

    def saveProcedure(self, obj, f):
        raise NotImplementedError('Call to abstract method.')

    def load(self):
        if not os.path.exists(self.filename):
            return {}

        try:
            f = open(self.filename, 'rb')
            try:
                obj = self.loadProcedure(f)
            finally:
                f.close()
        except IOError as e:
            message('Error reading file. Filename: {0}.\nAdditional exception info:\n{1}'.format(self.filename, str(e)))
            raise
        except Exception as e:
            message('Error occurred during deserialization. Filename: {0}.\nAdditional exception info:\n{1}'.format(self.filename, str(e)))
            raise

        return obj

    def loadProcedure(self, f):
        raise NotImplementedError('Call to abstract method.')


class SerializerFilePickle(SerializerFileBase):

    def __init__(self, *args, **kwargs):
        super(SerializerFilePickle, self).__init__(*args, **kwargs)

    def saveProcedure(self, obj, f):
        pickle.dump(obj, f, -1)

    def loadProcedure(self, f):
        return pickle.load(f)


class SerializerFileJson(SerializerFileBase):

    def __init__(self, *args, **kwargs):
        super(SerializerFileJson, self).__init__(*args, **kwargs)

    def saveProcedure(self, obj, f):
        json.dump(obj, f, sort_keys=True, indent=4, separators=(',', ': '))

    def loadProcedure(self, f):
        return json.load(f)


class SerializerOptVar(SerializerBase):

    def __init__(self, optVarName):
        if m is None:
            raise Exception('Cannot create SerializerOptVar: Maya is not available.')

        super(SerializerOptVar, self).__init__()
        self.optVarName = optVarName

    def save(self, obj):
        try:
            m.optionVar(stringValue=(self.optVarName, json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))))
        except Exception as e:
            message('Error occurred while saving option variable {0}.\nAdditional exception info:\n{1}'.format(self.optVarName, str(e)))
            raise

    def load(self):
        if not m.optionVar(exists=self.optVarName):
            return {}
        try:
            obj = json.loads(m.optionVar(q=self.optVarName))
        except Exception as e:
            message('Error occurred while loading option variable {0}.\nAdditional exception info:\n{1}'.format(self.optVarName, str(e)))
            raise
        return obj