import json
from lib.log import log_err, log_debug
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, USER, PASSWORD, VERSION, EMAIL

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        message = json.dumps({'operator':'register', 'user':username, 'password':PASSWORD, 'email':EMAIL})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ret = json.loads(ret)
        if not ret:
            log_err('%%%%%%%% register', 'failed to register %s, then register again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            ret = json.loads(ret)
            if not ret:
                ws.close()
                log_err('######## register', 'failed to register')
                return
        ws.close()
        cnt += 1
        log_debug('register', 'cnt=%d' % cnt)
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)