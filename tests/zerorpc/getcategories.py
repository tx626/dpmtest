import json
import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('get_categories', 'start testing ')
    for _ in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        info = cli.get_categories()
        cli.close()
        if not info:
            log_err('@@@@@@@@ get_categories', 'failed to get categories')
            return
        log_debug('get_categories', 'categories=%s' % str(json.loads(info)))
        if SHOW_TIME:
            log_debug('get_categories', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
