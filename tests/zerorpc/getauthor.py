from lib.log import log_debug, log_err
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, PKG_START, PACKAGE

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('get_author', 'start testing ')
    cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'operator':'get_author', 'package':package})
        ws = create_connection("ws://%s:%d/ws" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        if not ret:
            log_err('@@@@@@@@ get_author', 'failed to get the author of %s' % str(package))
        else:
            cnt += 1
        log_debug('get_author', 'cnt=%d' % cnt)
        #log_debug('get_author', 'the author of %s is %s' % (str(package), str(author)))
        if SHOW_TIME:
            log_debug('get_author', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)
