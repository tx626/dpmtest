import json
import zerorpc
from conf.dpmtest import PACKAGE
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PASSWORD, PKG_NUM

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('uninstall', 'start testing ')
    login_cnt = 0
    uninstall_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        username = USER + str(USER_START + i)
        user = json.dumps({'user':username, 'password':PASSWORD})
        uid, key = cli.login(user)
        if SHOW_TIME:
            log_debug('login', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
        if not uid or not key:
            log_err('%%%%%%%% login', 'failed to login %s. then login again.' % str(username))
            uid, key = cli.login(user)
            if not uid or not key:
                cli.close()
                log_err('######## login', 'failed to login')
                return
        login_cnt += 1
        if SHOW_TIME:
            start_time = datetime.utcnow()
        log_debug('login', 'cnt=%d' % login_cnt)
        num = randint(0, PKG_NUM - 1)
        package = PACKAGE + str(num)
        #package = PACKAGE + str(PKG_START + i)
        info = cli.uninstall(uid, package)
        cli.close()
        if not info:
            log_err('@@@@@@@@ uninstall', 'failed to uninstall app %s' % str(package))
            #return
        else:
            uninstall_cnt += 1
        log_debug('uninstall', 'cnt=%d' % uninstall_cnt)
        if SHOW_TIME:
            log_debug('uninstall', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
