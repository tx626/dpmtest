import json
import uuid
from lib.log import log_debug
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, EMAIL, PASSWORD

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    cnt = 0
    for _ in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = uuid.uuid4().hex
        message = json.dumps({'operator':'register', 'user':username, 'password':PASSWORD, 'email':EMAIL})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_debug('%%%%%%%%%%%%%%%%%%% register', 'failed to test')
            return
        cnt += 1
        log_debug('register', 'cnt=%d' % cnt)
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
