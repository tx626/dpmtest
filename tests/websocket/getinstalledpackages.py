import json
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PASSWORD, USER

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('get_installed_packages', 'start testing ')
    login_cnt = 0
    get_inst_pkgs_cnt = 0
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
            log_err('%%%%%%%% get_installed_packages->login', 'failed to login %s. then login again.' % str(username))
            ws.send(message)
            ret = ws.recv()
            result = json.loads(ret)
            uid = result[0]
            if not uid:
                ws.close()
                log_err('######## get_installed_packages->login', 'failed to login')
                return
        ws.close()
        if SHOW_TIME:
            log_debug('get_installed_packages->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('get_installed_packages->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'get_installed_packages', 'uid':uid})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        ret = json.loads(ret)
        if not ret:
            log_err('@@@@@@@@ get_installed_packages', 'failed to get installed packages')
            return
        else:
            get_inst_pkgs_cnt += 1
        log_debug('get_installed_packages', 'get_inst_pkgs_cnt=%d' % get_inst_pkgs_cnt)
        log_debug('get_installer_packages', 'installed packages are %s' % str(ret))
        if SHOW_TIME:
            log_debug('get_installed_packages', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
