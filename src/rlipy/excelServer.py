import argparse
import json
import sys
import time
import rlipy.zpull as zpull
import rlipy.zpub as zpub
from datetime import datetime
import zmq
import logging
import rlipy.logger
from enum import Enum
import rlipy.subscriptionManager as subscriptionManager
import copy
import re
class SubscribeMsgField(Enum):
    msgType = 0
    msgCategory = 1
    symbol =2
          
class ExcelServer(object):
    def __init__(self, name, jsonConfig, dataFeed):
        self.jsonConfig = jsonConfig        
        self.name = name
        self.datafeed = dataFeed
        self.cache = {} #map symbol to data
        self.sentMsgNo = 0
        self.sentMsgLastLoop = 0
        self.clientMsg = ''
        
        self.loadYesterdaySubscription()
        self.setEndTime(jsonConfig)
        self.setSockets(name, jsonConfig, subscriptionManager)

    def loadYesterdaySubscription(self):
        self.subscriptions = subscriptionManager.RedisSubscriptionManager(
            self.name, self.jsonConfig["redisHost"], int(self.jsonConfig["redisPort"]))

    def setEndTime(self, jsonConfig):
        tmp = datetime.strptime(jsonConfig['endTime'], "%H:%M:%S")
        now = datetime.now()
        self.endTime = datetime(now.year, now.month, now.day, tmp.hour, tmp.minute, tmp.second)

    def setSockets(self, name, jsonConfig, subscriptionManager):
        self.subscribeAddress = jsonConfig['subscribeAddress']
        self.publishAddress = jsonConfig['publishAddress']
        self.zcontext = zmq.Context()
        self.subSocket = zpull.zpull(self.zcontext, self.subscribeAddress)
        self.pubSocket = zpub.zpub(self.zcontext, self.publishAddress)
        logging.info("server %s bind subscribe socket to %s" % (self.name, self.subscribeAddress))
        logging.info("server %s bind publish socket to %s" % (self.name, self.publishAddress))

    def shutDown(self):
        logging.info("shutting down server")
        logging.info("stat: sentMsgNo=%d, cache=%d, subscribed=%d" % (
            self.sentMsgNo, len(self.cache), len(self.subscriptions.getAllSymbols())))
        self.subSocket.close()
        self.pubSocket.close()
        self.datafeed.shutDown()
        logging.info("server is down")

    def run(self):
        logging.info("starting excelserver")
        self.getSnapshotForYesterdaySymbols()
        self.loop()

    def getSnapshotForYesterdaySymbols(self):
        for symbol in self.subscriptions.getAllSymbols():
            self.subscribeToDataFeed( symbol)
        updates = self.datafeed.getAll()
        for update in updates:
            self.onData(update)

    def loop(self):
        now = datetime.now()
        while now < self.endTime:
            #logging.debug("start loop")
            self.pollClients()
            #logging.debug("polled client")
            self.pollPriceFeeds()
            #logging.debug("polled feeds")
            self.sleepIfNoNewData()
            #logging.debug("week up")
            now = datetime.now()

    def pollClients(self):
        self.clientMsg = self.subSocket.recv()
        while(self.clientMsg):
            logging.debug("recv msg from client: %s" % (self.clientMsg))
            tokens = re.split('\|', self.clientMsg)
            try:
                self.parseClientMessage(tokens)
            except:
                logging.error("%s failed to parse msg %s" % (self.name, self.clientMsg), 
                                  exc_info=True)
                continue
            self.clientMsg = self.subSocket.recv()

    def parseClientMessage(self, tokens):
        if (tokens[SubscribeMsgField.msgType.value] == 'R'):
            if (tokens[SubscribeMsgField.msgCategory.value] == 'S'):
                symbol = tokens[SubscribeMsgField.symbol.value]
                self.subscribe('', symbol)
            elif (tokens[SubscribeMsgField.msgCategory.value] == 'U'):
                symbol = tokens[SubscribeMsgField.symbol.value]
                self.unsubscribe('', symbol)


    def subscribe(self, client, symbol):
        if(not self.subscriptions.hasSymbol(symbol)):
            self.subscribeToDataFeed(symbol)
        elif(symbol in self.cache):
            logging.debug("snapshot %s" % (str(self.cache[symbol])))
            self.publishData(self.cache[symbol])
        self.subscriptions.addSymbol(symbol, client)

    def publishData(self, data):
        self.pubSocket.send('M|U|'+str(data))
        self.sentMsgNo += 1

    def subscribeToDataFeed(self, symbol):
        logging.debug("subscribeToDataFeed %s " % ( symbol))
        self.datafeed.subscribe(symbol)

        
    def unsubscribe(self, client, symbol):
        logging.debug("unsubscribe %s from %s" % ( symbol, client))
        self.subscriptions.removeSymbol(symbol, client)
    
    def pollPriceFeeds(self):
        self.updates = self.datafeed.getUpdates()
        for update in self.updates:
            self.onData(update)

    def onData(self, data):
        logging.debug("onData %s" % (str(data)))
        old = self.cache[data.symbol] if data.symbol in self.cache else None
        sameData = (old!=None and old==data)
        if(old is None):
            self.cache[data.symbol] = copy.copy(data)
        else:
            self.cache[data.symbol].merge(data)
        if( (not self.subscriptions.hasSymbol(data.symbol)) or sameData):
            return
        else:
            logging.debug("publish %s" % (str(self.cache[data.symbol])))
            self.publishData(self.cache[data.symbol])

    def sleepIfNoNewData(self):
        if (self.sentMsgLastLoop == self.sentMsgNo):
            time.sleep(1)
        else:
            self.sentMsgLastLoop = self.sentMsgNo
