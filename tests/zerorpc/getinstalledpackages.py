import json
import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PASSWORD, USER

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('get_installed_packages', 'start testing ')
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        username = USER + str(USER_START + i)
        user = json.dumps({'user':username, 'password':PASSWORD})
        uid, _ = cli.login(user)
        if not uid:
            log_err('get_installed_packages', 'failed to login %s, then login again' % str(username))
            uid, _ = cli.login(user)
            if not uid:
                cli.close()
                log_err('######## get_installed_packages', 'failed to login %s' % str(username))
                return
        info = cli.get_installed_packages(uid)
        cli.close()
        if not info:
            log_err('@@@@@@@@ get_installed_packages', 'failed to get installed packages')
            return
        log_debug('get_installer_packages', 'install packages are %s' % str(json.loads(info)))
        if SHOW_TIME:
            log_debug('get_installed_packages', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
