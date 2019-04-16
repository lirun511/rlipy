class Price(object):
    def __init__(self):
        self.symbol = ''
        self.clear()
        
    def clear(self):
        self.bidPrice = ''
        self.bidSpread = ''
        self.benchmark = ''
        self.askPrice = ''
        self.askSpread = ''
        self.benchmark = ''
        self.time = ''
        self.flags = ''
        return self
        
    def invalidatePrice(self):
        self.bidPrice = ''
        self.bidSpread = ''
        self.benchmark = ''
        self.askPrice = ''
        self.askSpread = ''
        self.benchmark = ''
        return self
        
    def __str__(self):
        # 4 stand of IDSource ISIN
        return  '%s|%s|%s|%s|4|%s|%s|%s|4|%s|%s' % (self.symbol,
             self.bidPrice, self.bidSpread, self.benchmark,
             self.askPrice, self.askSpread, self.benchmark,
             self.time,
             self.flags
             )
    def merge(self, other):
        for k,v in list(other.__dict__.items()):
            self.__setattr__(k, v)
                
    def __eq__(self, other):
        if(other == None): return False
        return self.__dict__ == other.__dict__

class DataFeedBase(object):
    def __init__(self, jsonConfig):
        self.jsonConfig = jsonConfig

    def subscribe(self, symbol):
        raise NotImplementedError

    def unsubscribe(self, symbol):
        raise NotImplementedError
