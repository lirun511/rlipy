
class DataFeedBase(object):
    def __init__(self, jsonConfig):
        self.jsonConfig = jsonConfig

    def subscribe(self, symbol):
        raise NotImplementedError

    def unsubscribe(self, symbol):
        raise NotImplementedError
