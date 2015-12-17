import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port, PACKAGE
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, PASSWORD, USER

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cli = zerorpc.Client()
        cli.connect('tcp://%s:%d' % (get_manager(), get_port()))
        username = USER + str(USER_START + i)
        user = json.dumps({'user':username, 'password':PASSWORD})
        uid, key = cli.login(user)
        if uid and key:
            package = PACKAGE + str(PKG_START + i)
            if not cli.has_package(uid, package):
                log_err('has_package', 'failed to has app %s' % str(package))
        else:
            log_err('%%%%%%%%%%%%%%%%%%% has_package', 'failed to test')
        cli.close()
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
