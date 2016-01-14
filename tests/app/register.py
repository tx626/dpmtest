#      register.py
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
from lib.log import log_err, log_debug
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, USER, PASSWORD, VERSION, EMAIL

if SHOW_TIME:
    from datetime import datetime

def test():
    log_debug('register', 'start testing ')
    register_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        message = json.dumps({'operator':'register', 'user':username, 'password':PASSWORD, 'email':EMAIL})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'register' != result['operator'] or username != result['user'] or not  result['data']:
            log_err('register', 'failed to register %s.' % str(username))
            return False
        register_cnt += 1
        log_debug('register', 'register_cnt=%d' % register_cnt)
        if SHOW_TIME:
            log_debug('register', 'test, time=%d sec' % (datetime.utcnow() - start_time).seconds)