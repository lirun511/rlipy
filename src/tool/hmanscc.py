'''
Created on Apr 26, 2017
@author: rli
'''

import os
import datetime
import pandas as pd
import argparse
import re
import traceback
import redis
import logging
import json
import math
import rlipy.util as util
import rlipy.logger

hmaDailyDir = '/data/prod/hma/daily'
hmaTodayDir = hmaDailyDir+'/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')  
try:
    os.makedirs(hmaTodayDir)
    util.make_link(hmaTodayDir, hmaDailyDir+'/today')
    os.chmod(hmaTodayDir, 0775)
except:
    pass

import rlipy.nscc as nscc
import rlipy.util as util
import rlipy.tradedate as td
"""
HYG    Date
nav_per_etf    etf_shares_per_cu
total_cash_amt_per_cu    est_t-1_cash_amt_per_cu
CUSIP    QUANTITY
"""
def etf_wanted():
    fn = hmaDailyDir + '/etf.csv'
    etf_list = pd.read_csv(fn)
    return etf_list['TICKER'].drop_duplicates().tolist()

class Component(object):
    def __init__(self):
        self.etf_symbol = ''
        self.trade_date = ''
        self.id = ''
        self.id_type = 'Unknown'
        self.quantity = ''
        self.description = ''
        self.cash_in_lieu_ind = 'N'
        
class ETF(object):
    id_type_mapping = {
        # comp_id_code '1' for cusip; '2' for sedol;
        # '3' for isin; '4' for isin+sedol
        1: 'CUSIP',
        2: 'SEDOL',
        3: 'ISIN',
        4: 'ISIN'
        }
    def __init__(self):
        self.etf_symbol = ''
        self.trade_date = ''
        self.nav_per_etf = 0.0
        self.etf_shares_per_cu = 0
        self.total_cash_amt_per_cu = 0
        self.est_cash_amt_per_cu = 0.0
        self.components = []
        
    def write_redis(self, redis_prefix, redis_db):
        basket_key = redis_prefix+":BASKET:"+self.etf_symbol
        component_key = redis_prefix+":COMPONENT:"+self.etf_symbol
        redis_db.delete(basket_key)
        redis_db.delete(component_key)
        logging.info("deleted %s basket from redis" % basket_key)
        d = dict(self.__dict__)
        del d['components']
        redis_db.set(basket_key, json.dumps(d))
        for component in self.components:
            redis_db.hset(component_key, component.id, json.dumps(component.__dict__))
     
    def __str__(self):
        s = '%s,%s\n%f,%d\n%f,%f\n' % (self.etf_symbol, self.trade_date,
                                       self.nav_per_etf, self.etf_shares_per_cu,
                                       self.total_cash_amt_per_cu, self.est_cash_amt_per_cu
                                       )
        for c in self.components:
            if(c.id == 'USD'):
                s += '%s,%d\n' % (c.id, c.quantity)
        for c in self.components:
            if(c.id != 'USD'):
                #id = re.sub('\/.*\/', '', c.id)
                s += '%s,%d\n' % (c.id, c.quantity)
        return s
    
    def set_basket(self, s):
        self.etf_symbol = s['etf_symbol']
        self.trade_date = s['trade_date']
        self.nav_per_etf = s['nav_per_etf']
        self.etf_shares_per_cu = s['etf_shares_per_cu']
        self.total_cash_amt_per_cu = s['total_cash_amt_per_cu']
        self.est_cash_amt_per_cu = s['est_t-1_cash_amt_per_cu'] 
             
    def get_query_id(self, s):
        try:
            # comp_id_code '1' for cusip; '2' for sedol;
            # '3' for isin; '4' for isin+sedol
            if(s['comp_id_code'] == 4):  # isin+sedol
                return s['comp_id'][0:12]
            else:
                return s['comp_id']
        except:
            return None
         
    def get_quantity(self, ss):
        try:
            if ss['sign_comp_quantity'] == '-':
                sign = -1
            else:
                sign = 1
            quantity = util.to_int(util.num(ss['comp_quantity']) * sign)
            return quantity
        except:
            logging.error("failed to get quantity for %s %s" % (ss['etf_symbol'], ss['comp_id']))
            logging.error(traceback.format_exc())
            raise
        
    def add_component(self, ss):        
        comp = Component()
        comp.id = ss['QUERY_ID']
        if(util.to_int(ss['comp_id_code']) in ETF.id_type_mapping):
            comp.id_type = ETF.id_type_mapping[ss['comp_id_code']]
        comp.quantity = self.get_quantity(ss)
        comp.description = ss['comp_description']
        if((not (comp.description)) or comp.description!=comp.description):
            comp.description = ''
        comp.cash_in_lieu_ind = ss['cash_in_lieu_ind']
        if((not (comp.cash_in_lieu_ind)) or comp.cash_in_lieu_ind!=comp.cash_in_lieu_ind):
            comp.cash_in_lieu_ind = 'N'
        comp.etf_symbol = self.etf_symbol
        comp.trade_date = self.trade_date
        self.components.append(comp)
    
    def set_components(self, ss):
        sub = ss[ss['etf_symbol'] == self.etf_symbol]
        sub = sub.sort_values(by=['comp_description'])
        ss['QUERY_ID'] = ss.apply(lambda s: self.get_query_id(s), axis=1)
        ss = ss.sort_values(by=['comp_description'])
        ss.apply(lambda x:self.add_component(x), axis=1)
    
    @staticmethod
    def create_etf(basket, components):
        if(basket['etf_symbol'] in ['JNK', 'SJNK', 'SPSB']):
            etf = CilEtf()
        else:
            etf = ETF()
        etf.set_basket(basket)
        etf.set_components(components[components['etf_symbol'] == etf.etf_symbol])
        return etf
            
    @staticmethod
    def read_nscc(baskets, components_raw, etf_list=None):
        if(etf_list is not None):
            baskets = baskets[baskets['etf_symbol'].isin(etf_list)]
        components = pd.merge(components_raw, baskets[['portfolio_id', 'etf_symbol']].drop_duplicates(), on=['portfolio_id'])
        etfs = baskets.apply(lambda x: ETF.create_etf(x, components), axis=1)
        etfs = etfs.tolist()
        return etfs

class CilEtf(ETF):
    def __str__(self):
        s = '%s,%s\n%f,%d\n%f,%f\n' % (self.etf_symbol, self.trade_date,
                                       self.nav_per_etf, self.etf_shares_per_cu,
                                       self.total_cash_amt_per_cu, self.est_cash_amt_per_cu
                                       )
        # we output cash first for CilEtf
        try:
            for comp in self.components:
                if(comp.id == 'USD'):
                    s += '%s,%d,%s\n' % (comp.id, comp.quantity, '')
                    # s += '%s,%d,%s,%s\n' % (comp.id, comp.quantity, comp.description, '')
            for comp in self.components:
                if(comp.cash_in_lieu_ind == 'Y' and comp.id != 'USD'):
                    s += '%s,%d,%s\n' % (re.sub('\/.*\/', '', comp.id), comp.quantity, comp.cash_in_lieu_ind)
                    # s += '%s,%d,%s,%s\n' % (re.sub('\/.*\/', '', comp.id), comp.quantity, comp.description, comp.cash_in_lieu_ind)
            for comp in self.components:
                if(comp.cash_in_lieu_ind != 'Y'):
                        s += '%s,%d,%s\n' % (re.sub('\/.*\/', '', comp.id), comp.quantity, '')
                        # s += '%s,%d,%s,%s\n' % (re.sub('\/.*\/', '', comp.id), comp.quantity, comp.description,'')
        except:
            logging.error("failed to get CilEtf " + self.etf_symbol + " " + comp.id)
        return s

def main():
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=today, type=str, help="locate date")
    parser.add_argument("-s", "--redis_server_host")
    parser.add_argument("-p", "--redis_server_port")
    args = parser.parse_args()
    redis_db = None
    trade_date = args.date
    cal = td.TradeDate('US')
    file_date = cal.previous_day_str(args.date)
    if(args.redis_server_port):
        try:
            redis_port = int(args.redis_server_port)
            logging.info("connecting to redis %s %d" % (args.redis_server_host, redis_port))
            redis_db = redis.StrictRedis(args.redis_server_host, redis_port)
        except:
            logging.error("failed to write to redis %s %d" % (args.redis_server_host, redis_port))
    etf_list = etf_wanted()
    
    logging.info("start reading nscc files %s" % (nscc.nscc_raw_file(file_date)))
    baskets = nscc.get_nscc_basket(nscc.nscc_raw_file(file_date))
    components_raw = nscc.get_nscc_component(nscc.nscc_raw_file(file_date))
    logging.info("finished reading nscc files")
    etfs = ETF.read_nscc(baskets, components_raw, etf_list)
    logging.info("created etfs")
    fileHandler = None
    output_file = hmaTodayDir + '/all.csv'
    try:
        os.umask(000)
        util.hma_make_today_dir()
        fileHandler = open(output_file, 'w+')
    except:
        logging.error("failed to create output file %s" %  (output_file),  exc_info=True)
    if(fileHandler):
        try:
            for etf in etfs:
                fileHandler.write(str(etf))
                fileHandler.write('\n')
            fileHandler.close()
            logging.info("finished writing files")  
            baskets.to_csv(hmaTodayDir + '/nsccbasket.csv', index=False)
            components_raw.to_csv(hmaTodayDir + '/nscccomponent.csv', index=False)
        except:
            logging.error("failed to write to file %s" % (output_file))

    if(redis_db):
        try:     
            for etf in etfs:
                etf.write_redis(redis_db)
            logging.info("finished writing redis")  
        except:
            logging.error("failed to write to redis %s %d" % (args.redis_server_host, args.redis_server_port))
        
