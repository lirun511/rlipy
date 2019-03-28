'''
Created on Nov 4, 2016

@author: rli
'''
import sys
import os
from datetime import datetime
BBQ_HOST               = 'rli02-w7'
BBQ_PORT               = '7200'
BBQ_PORT_2             = '5555'
BBQ_PORT_3             = '5555'

IS_WINDOWS = sys.platform.find('win')==0
if(IS_WINDOWS):
    DATA_DIR = 'R:'
else:
    DATA_DIR = '/data'
if(os.environ.has_key('PYTHONTEST') and os.environ['PYTHONTEST']=='1'):
    DATA_DIR = DATA_DIR+'/common/rli/testdata'

ROOT_DIR = DATA_DIR+'/prod/infra'
SECMAST_DIR = ROOT_DIR+'/secmast'


HMA_DAILY_DIR = DATA_DIR+'/prod/hma/daily'
HMA_TODAY_DIR = HMA_DAILY_DIR + '/' + datetime.strftime(datetime.now(), '%Y%m%d')    
