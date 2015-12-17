import json
from random import randint
from conf.dpmtest import PACKAGE
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port, APP
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PASSWORD, VERSION, PKG_NUM, CATEGORY

if SHOW_TIME:
    from datetime import datetime

def test():
    #log_debug('install', 'start testing ')
    login_cnt = 0
    install_cnt = 0
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
            log_err('%%%%%%%% install->login', 'failed to login %s. then login again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            result = json.loads(ret)
            uid = result[0]
            key = result[1]
            if not uid or not key:
                ws.close()
                log_err('######## install->login', 'failed to login')
                return
        ws.close()
        if SHOW_TIME:
            log_debug('install->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('install->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        num = randint(0, PKG_NUM - 1)
        package = PACKAGE + str(num)
        #package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'operator':'install', 'uid':uid, 'package':package, 'version':VERSION, 'typ':APP})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_err('@@@@@@@@ install', 'failed to install app %s' % str(package))
            #return
        else:
            install_cnt += 1
        log_debug('install', 'install_cnt=%d' % install_cnt)
        if SHOW_TIME:
            log_debug('install', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
    
    message = json.dumps({'operator':'get_top', 'category':CATEGORY})
    ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
    ws.send(message)
    ret = ws.recv()
    ws.close()
    ret = json.loads(ret)
    if ret:
        log_debug('get_top', 'packages=%s' % str(ret))
    else:
        log_err('######## get_top', 'failed to get top')
    
    message = json.dumps({'operator':'get_top_details', 'category':CATEGORY})
    ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
    ws.send(message)
    ret = ws.recv()
    ws.close()
    ret = json.loads(ret)
    if ret:
        log_debug('get_top_details', 'packages=%s' % str(ret))
    else:
        log_err('$$$$$$$$ get_top_details', 'failed to get top details')
    