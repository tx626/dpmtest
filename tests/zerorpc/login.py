import json
import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
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
        user = json.dumps({'user':username, 'password':PASSWORD})
        #log_debug('register', 'user=%s' % str(user))
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        uid, key = cli.login(user)
        if not uid or not key:
            log_err('%%%%%%%% login', 'failed to login %s. then login again.' % str(username))
            uid, key = cli.login(user)
            if not uid or not key:
                cli.close()
                log_err('######## login', 'failed to login')
                return
        cli.close()
        cnt += 1
        log_debug('install', 'cnt=%d' % cnt)
        if SHOW_TIME:
            log_debug('login', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
