# noinspection PyBroadException
try:
    import cPickle as pickle
except:
    import pickle

from com import message


class SerializerFile(object):

    def __init__(self, filename):
        pass


def pickleSave(obj, filename):
    try:
        f = open(filename, 'wb')
        try:
            pickle.dump(obj, f, -1)
        finally:
            f.close()
    except IOError as e:
        message(
            text='Error writing file.',
            textInformative='Filename: ' + filename,
            textDetailed='Additional exception info:\n' + str(e))
        raise
    except Exception as e:
        message(
            text='Unknown error occurred while saving the file.',
            textInformative='Filename: ' + filename,
            textDetailed='Additional exception info:\n' + str(e))
        raise


def pickleLoad(filename):
    try:
        f = open(filename, 'rb')
        try:
            obj = pickle.load(f)
        finally:
            f.close()
    except IOError as e:
        message(
            text='Error reading file.',
            textInformative='Filename: ' + filename,
            textDetailed='Additional exception info:\n' + str(e))
        raise
    except Exception as e:
        message(
            text='Unknown error occurred while reading the file.',
            textInformative='Filename: ' + filename,
            textDetailed='Additional exception info:\n' + str(e))
        raise

    return obj