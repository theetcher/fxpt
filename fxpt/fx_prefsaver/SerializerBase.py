class SerializerBase(object):

    def __init__(self):
        pass

    def save(self, prefData):
        raise NotImplementedError('Call to abstract method')

    def load(self):
        raise NotImplementedError('Call to abstract method')

    def reset(self):
        raise NotImplementedError('Call to abstract method')
