import json
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port, PACKAGE
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    get_top_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'get_top', 'category':CATEGORY})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_err('%%%%%%%% get_top', 'failed to get the top packages of %s' % str(CATEGORY))
            return
        else:
            get_top_cnt +=1
        log_debug('get_top', 'get_top_cnt=%d' % get_top_cnt)
        log_debug('get_top', 'packages=%s' % str(ret))
        if SHOW_TIME:
            log_debug('register', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
