import json
from random import randint
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

PAGE_SIZE = 3

def test():
    log_debug('register', 'start testing ')
    get_pkgs_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'get_counter', 'category':CATEGORY})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        counter = json.loads(ret)
        if not counter:
            log_err('%%%%%%%% get_packages->get_counter', 'failed to get the total number of %s ' % str(CATEGORY))
            return
        if SHOW_TIME:
            log_debug('get_packages->get_counter', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        rank = randint(0, (counter  + PAGE_SIZE  - 1) / PAGE_SIZE - 1)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'get_packages', 'category':CATEGORY, 'rank':rank})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_err('######## get_packages', 'failed to get packages')
            return
        get_pkgs_cnt += 1
        log_debug('get_packages', 'get_pkgs_cnt=%d' % get_pkgs_cnt)
        log_debug('get_packages', 'packages=%s' % str(ret))
        if SHOW_TIME:
            log_debug('get_packages', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
