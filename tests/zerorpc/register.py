import json
import uuid
import zerorpc
from lib.log import log_debug
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, EMAIL, PASSWORD

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    for _ in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = uuid.uuid4().hex
        user = json.dumps({'user':username, 'password':PASSWORD, 'email':EMAIL})
        #log_debug('register', 'user=%s' % str(user))
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        ret = cli.register(user)
        cli.close()
        if ret ==  str(False):
            log_debug('%%%%%%%%%%%%%%%%%%% register', 'failed to test')
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
