#      haspackage.py
#      
#      Copyright (C) 2015 Xu Tian <tianxu@iscas.ac.cn>
#      
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#      
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#      
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#      MA 02110-1301, USA.

import json
from lib.log import log_debug, log_err
from websocket import create_connection
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, PASSWORD, USER, PACKAGE

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
        ws.close()
        result = json.loads(ret)
        if not result or 'login' != result['operator'] or username != result['user'] or not  result['data']:
            log_err('login', 'failed to login %s.' % str(username))
            return False
        uid = result['data'][0]
        if not uid:
            log_err('has_package->login', 'failed to login %s, invalid uid or key.' % str(username))
            return False
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
        result = json.loads(ret)
        if not result or 'has_package' != result['operator'] or package != result['package'] or not  result['data']:
            log_err('has_package', 'failed to install app %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('has_package', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        has_pkg_cnt += 1
        log_debug('has_package', 'has_pkg_cnt=%d' % has_pkg_cnt)
        