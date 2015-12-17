import json
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('get_categories', 'start testing ')
    cat_cnt = 0
    for _ in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'get_categories'})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ret = json.loads(ret)
        ws.close()
        if not ret:
            log_err('@@@@@@@@ get_categories', 'failed to get categories')
            return
        else:
            cat_cnt += 1
        log_debug('get_categories', 'cat_cnt=%d' % cat_cnt)
        log_debug('get_categories', 'categories=%s' % str(ret))
        if SHOW_TIME:
            log_debug('get_categories', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
