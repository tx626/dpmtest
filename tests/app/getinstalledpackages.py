#      getinstalledpackages.py
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
        ws.close()
        result = json.loads(ret)
        if not result or 'login' != result['operator'] or username != result['user'] or not  result['data']:
            log_err('get_installed_packages->login', 'failed to login %s.' % str(username))
            return False
        uid = result['data'][0]
        if not uid:
            log_err('get_installed_packages->login', 'failed to login %s, invalid uid.' % str(username))
            return False
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
        result = json.loads(ret)
        if not result or 'get_installed_packages' != result['operator'] or uid != result['uid']:
            log_err('get_installed_packages', 'failed to get installed packages')
            return False
        get_inst_pkgs_cnt += 1
        log_debug('get_installed_packages', 'get_inst_pkgs_cnt=%d' % get_inst_pkgs_cnt)
        log_debug('get_installer_packages', 'installed packages are %s' % str(result['data']))
        if SHOW_TIME:
            log_debug('get_installed_packages', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
