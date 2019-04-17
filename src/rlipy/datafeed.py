
class DataFeedBase(object):
    def __init__(self, jsonConfig):
        self.jsonConfig = jsonConfig

    def subscribe(self, symbol):
        raise NotImplementedError
    
    def getUpdates(self):
        raise NotImplementedError

    def shutDown(self):
        raise NotImplementedError