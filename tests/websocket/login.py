import json
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, USER, PASSWORD

if SHOW_TIME:
    from datetime import datetime

def test():
    #log_debug('login', 'start testing ')
    cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        message = json.dumps({'operator':'login', 'user':username, 'password':PASSWORD})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        result = json.loads(ret)
        uid = result[0]
        key = result[1]
        if not uid or not key:
            log_err('%%%%%%%% login', 'failed to login %s. then login again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            result = json.loads(ret)
            uid = result[0]
            key = result[1]
            if not uid or not key:
                ws.close()
                log_err('######## login', 'failed to login')
                return
        ws.close()
        cnt += 1
        log_debug('login', 'cnt=%d' % cnt)
        if SHOW_TIME:
            log_debug('login', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
