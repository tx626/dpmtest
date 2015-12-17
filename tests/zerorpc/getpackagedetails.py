import json
import zerorpc
from random import randint
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        rank = randint(0, PAGE - 1)
        info = cli.get_package_details(CATEGORY, rank)
        cli.close()
        if not info:
            log_err('@@@@@@@@ get_package_details', 'failed to get package details')
            return
        log_debug('get_package_details', 'packages=%s' % str(json.loads(info)))
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)


   
        