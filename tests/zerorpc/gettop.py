import json
import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port, PACKAGE
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
        res = cli.get_top(CATEGORY)
        if res:
            log_debug('get_top', 'packages=%s' % str(json.loads(res)))
        else:
            log_err('%%%%%%%%%%%%%%%%%%% get_top', 'failed to test')
        cli.close()
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
