import json
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port, PACKAGE
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, PASSWORD, USER

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    login_cnt = 0
    has_pkg_cnt = 0
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
        if not uid:
            log_err('%%%%%%%% has_package->login', 'failed to login %s. then login again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            result = json.loads(ret)
            uid = result[0]
            if not uid:
                ws.close()
                log_err('######## has_package->login', 'failed to login')
                return
        ws.close()
        if SHOW_TIME:
            log_debug('has_package->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('has_package->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'operator':'has_package', 'uid':uid,'package':package})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_err('has_package', 'failed to has app %s' % str(package))
            return
        else:
            has_pkg_cnt += 1
        log_debug('has_package', 'has_pkg_cnt=%d' % has_pkg_cnt)
        log_debug('has_package', 'packages=%s' % str(ret))
        if SHOW_TIME:
            log_debug('has_package', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
