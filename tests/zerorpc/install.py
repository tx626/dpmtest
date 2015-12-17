import json
import zerorpc
from random import randint
from conf.dpmtest import PACKAGE
from lib.log import log_debug, log_err
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
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        username = USER + str(USER_START + i)
        user = json.dumps({'user':username, 'password':PASSWORD})
        uid, key = cli.login(user)
        if SHOW_TIME:
            log_debug('install', 'login, time=%d sec' % (datetime.utcnow() - start_time).seconds)
        if not uid or not key:
            log_err('%%%%%%%% login', 'failed to login %s, then login again.' % str(username))
            uid, key = cli.login(user)
            if not uid or not key:
                cli.close()
                log_err('######## login', 'failed to login')
                return
        login_cnt += 1
        log_debug('login', 'cnt=%d' % login_cnt)
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        num = randint(0, PKG_NUM - 1)
        package = PACKAGE + str(num)
        #package = PACKAGE + str(PKG_START + i)
        info = cli.install(uid, package, VERSION, APP)
        cli.close()
        if not info:
            log_err('@@@@@@@@ install', 'failed to install app %s' % str(package))
            #return
        else:
            install_cnt += 1
        log_debug('install', 'cnt=%d' % install_cnt)
        if SHOW_TIME:
            log_debug('install', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
    cli = zerorpc.Client()
    cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
    res = cli.get_top(CATEGORY)
    if res:
        log_debug('get_top', 'packages=%s' % str(json.loads(res)))
    else:
        log_err('%%%%%%%%%%%%%%%%%%% get_top', 'failed to get top')
    res = cli.get_top_details(CATEGORY)
    if res:
        log_debug('get_top_details', 'packages=%s' % str(json.loads(res)))
    else:
        log_err('%%%%%%%%%%%%%%%%%%% get_top_details', 'failed to get top details')
    cli.close()
    