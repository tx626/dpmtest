import json
import zerorpc
from random import randint
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

PAGE_SIZE = 3

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        counter = cli.get_counter(CATEGORY)
        rank = randint(0, (counter  + PAGE_SIZE  - 1) / PAGE_SIZE - 1)     
        res = cli.get_packages(CATEGORY, rank)
        cli.close()
        if res:
            log_debug('get_packages', 'packages=%s' % str(json.loads(res)))
        else:
            log_err('%%%%%%%%%%%%%%%%%%% get_packages', 'failed to test')
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
