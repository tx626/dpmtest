import json
import zerorpc
from lib.log import log_debug, log_err
from lib.util import get_manager, get_port, login, upload, APP
from conf.dpmtest import  TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PACKAGE, PASSWORD, VERSION

PATH = '/root/testfiles/pkgapp8'

if SHOW_TIME:
    from datetime import datetime

def test():
    #log_debug('upload', 'start testing ')
    login_cnt = 0
    upload_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        uid, key = login(username, PASSWORD)
        if not uid or not key:
            log_err('%%%%%%%% login', 'failed to login %s. then login again.' % str(username))
            uid, key = login(username, PASSWORD)
            if not uid or not key:
                log_err('######## login', 'failed to login')
                return
        login_cnt += 1
        log_debug('login', 'cnt=%d' % login_cnt)
        package = PACKAGE + str(PKG_START + i)
        if upload(PATH, uid, package, VERSION, APP, key):
            upload_cnt += 1
        else:
            if upload(PATH, uid, package, VERSION, APP, key):
                upload_cnt += 1
            else:
                log_err('@@@@@@@@ upload', 'failed to upload app %s' % str(package))
                #return
        #log_debug('upload', 'upload app %s successfully' % str(package))
        log_debug('upload', 'cnt=%d' % upload_cnt)
        if SHOW_TIME:
            log_debug('upload', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
