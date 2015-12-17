import json
from conf.dpmtest import PACKAGE
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
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
        username = USER + str(USER_START + i)
        message = json.dumps({'operator':'login', 'user':username, 'password':PASSWORD})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        result = json.loads(ret)
        uid = result[0]
        key = result[1]
        if not uid or not key:
            log_err('%%%%%%%% uninstall->login', 'failed to login %s. then login again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            result = json.loads(ret)
            uid = result[0]
            key = result[1]
            if not uid or not key:
                ws.close()
                log_err('######## uninstall->login', 'failed to login')
                return
        ws.close()
        if SHOW_TIME:
            log_debug('uninstall->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('uninstall->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        num = randint(0, PKG_NUM - 1)
        package = PACKAGE + str(num)
        #package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'operator':'uninstall', 'package':package})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ret = json.loads(ret)
        if not ret:
            log_err('@@@@@@@@ uninstall', 'failed to uninstall app %s' % str(package))
            #return
        else:
            uninstall_cnt += 1
        log_debug('uninstall', 'uninstall_cnt=%d' % uninstall_cnt)
        if SHOW_TIME:
            log_debug('uninstall', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
