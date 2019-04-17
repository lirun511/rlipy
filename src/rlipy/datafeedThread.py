from . import datafeed
import logging
from queue import Queue, Empty
import threading 

class DataFeedThread(datafeed.DataFeedBase):
    def __init__(self, datafeedImpl):
        self.datafeedImpl = datafeedImpl
        self.subscribeQueue = Queue()
        self.updateQueue = Queue()
        self.killed = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def subscribe(self, symbol):
        self.subscribeQueue.put(symbol)
    
    def getAll(self):
        return self.datafeedImpl.getAll()
        
    def getUpdates(self):
        updates = []
        try:
            updates.append(self.updateQueue.get_nowait())
        except Empty:
            pass
        return updates
    
    def shutDown(self):
        self.killed = True
    
    def processSubscribes(self):
        subscribes_ = []
        try:
            while True:
                newSubscribe = self.subscribeQueue.get_nowait()
                self.datafeedImpl.subscribe(newSubscribe)
        except Empty:
            pass
    
    def run(self):
        while(not self.killed):
            try:
                self.processSubscribes()
                updates = self.datafeedImpl.getUpdates()
                for u in updates:
                    self.updateQueue.put(u)
            except :
                logging.error("DataFeedThread main loop error", exc_info=True)
            
 