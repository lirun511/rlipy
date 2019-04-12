'''
Created on Nov 9, 2016

@author: rli
'''
import re
import pandas as pd
import subprocess
import logging
import os
import uuid
import rlipy.env as env
import time
import datetime

def to_int(s):
    try:
        return int(s)
    except:
        return 0
def num(s):
    try:
        return float(s)
    except:
        return 0

def num_or_nah(s):
    try:
        return float(s)
    except:
        return None

def format_num(f):
    abs_val = abs(f)
    if(abs_val==0):
        return '0'
    elif(abs_val<1):
        return '{:.4f}'.format(f)
    elif(abs_val<1000):
        return '{:.1f}'.format(f)
    elif(abs_val<1000000):
        return '{:,.0f}'.format(f)
    else:
        return '{:.2f}m'.format(f/1000000.0)

def sync_run(cmd_and_arg):
    try:
        ret = re.split('\n', subprocess.check_output(cmd_and_arg, shell=True))
    except subprocess.CalledProcessError :
        #print "ERROR %s" % (e)
        return []
    return ret

def pandas_run(cmd_and_arg, sep=' ', header=None):
    text_list = sync_run(cmd_and_arg)
    if(header is None):
        header = []
        if(len(text_list)==0):
            return pd.DataFrame()
        header = re.split(sep, text_list.pop(0))
    tuple_list = []
    lnum = 0
    for line in text_list:
        lnum += 1
        if(len(line)==0):
            continue
        tuples = re.split(sep, line);
        if(len(tuples)==len(header)):
            tuple_list.append(tuples)
        elif(len(tuples)>0):
            logging.warn('pandas_run "%s" skip line#%d: %s' % (cmd_and_arg, lnum, line))
    if(len(tuple_list)==0):
        return pd.DataFrame(columns=header)
    else:
        return pd.DataFrame(tuple_list, columns=header)

def tzdiff(timeZoneName):
    cur=time.time()
    myTime = time.localtime(cur)
    orig = os.environ["TZ"] if 'TZ' in os.environ else None
    os.environ["TZ"] = timeZoneName
    tzTime = time.localtime(cur)
    if(orig==None) :
        del os.environ["TZ"]
    else: 
        os.environ["TZ"] = orig  
    
    delta = (datetime.datetime(tzTime.tm_year, tzTime.tm_mon, tzTime.tm_mday, tzTime.tm_hour, tzTime.tm_min, tzTime.tm_sec)- 
            datetime.datetime(myTime.tm_year, myTime.tm_mon, myTime.tm_mday, myTime.tm_hour, myTime.tm_min, myTime.tm_sec))
    return delta

def make_link(src, link):
    tmp = os.path.dirname(link)+'/'+str(uuid.uuid4())
    os.symlink(src, tmp)
    os.rename(tmp, link)
    
def hma_make_today_dir():
    if(not os.path.isdir(env.HMA_TODAY_DIR)):
        today_link =  env.HMA_DAILY_DIR+'/today'
        os.mkdir(env.HMA_TODAY_DIR)
        make_link(env.HMA_TODAY_DIR, today_link)
