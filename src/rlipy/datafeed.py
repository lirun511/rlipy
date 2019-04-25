

class DataFeedBase(object):

    def subscribe(self, symbol):
        raise NotImplementedError

    def getUpdates(self):
        raise NotImplementedError

    def shutDown(self):
        raise NotImplementedError
