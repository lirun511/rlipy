import logging
import os
import datetime
import __main__
if 'LOG_DIR' not in os.environ:
    log_dir = './log/'+datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d');
else:
    log_dir = os.environ['LOG_DIR']+'/'+datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d');
try:
    os.makedirs(log_dir)
except:
    pass
if('__file__' in __main__.__dict__):
    log_file = log_dir+'/'+os.path.splitext(os.path.basename(__main__.__file__))[0]+'.log'
else:
    log_file = log_dir+'/'+'python.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                        format='%(asctime)s.%(msecs)d %(levelname)-5s [%(pathname)s:%(lineno)d] %(message)s',
                        datefmt='%H:%M:%S')
