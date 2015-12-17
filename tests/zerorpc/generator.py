import json
import zerorpc
from lib.log import log_err, log_debug
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START,  USER, PASSWORD, VERSION, EMAIL

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        user = json.dumps({'user':username, 'password':PASSWORD, 'email':EMAIL})
        #log_debug('register', 'user=%s' % str(user))
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        ret = cli.register(user)
        if ret ==  str(False):
            log_err('%%%%%%%% register', 'failed to register %s, then register again.' % str(username))
            info = cli.register(user)
            if info == str(False):
                cli.close()
                log_err('######## register', 'failed to register')
                return
        cli.close()
        cnt += 1
        log_debug('register', 'cnt=%d' % cnt)
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
