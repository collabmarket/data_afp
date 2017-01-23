from __future__ import print_function
import os
from datetime import datetime

def logg_info(msg, tipo='INFO', status='OK'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("[%s]--%s--%s--%s" % (tipo, timestamp, msg, status))

def makedir(dirname, by=__file__):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        logg_info('%s mkdir %s' % (by, dirname), tipo='INFO', status='OK')
