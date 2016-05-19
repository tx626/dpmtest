#      install.py
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
from random import randint
from lib.log import log_debug, log_err
from conf.category import CATEGORIES
from websocket import create_connection
from lib.util import get_manager, get_port, APP
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER_START, PKG_START, USER, PACKAGE, PASSWORD, VERSION, PKG_NUM, CATEGORY

if SHOW_TIME:
    from datetime import datetime

PKG = 'bbb3'
CAT = ['cat0']
RANDOM_PKG = True

def test():
    log_debug('install', 'start testing ')
    login_cnt = 0
    install_cnt = 0
    has_pkg_cnt = 0
    get_top_cnt = 0
    get_top_details_cnt = 0
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
        key = result['data'][1]
        if not uid or not key:
            log_err('install->login', 'failed to login %s, invalid uid or key.' % str(username))
            return False
        if SHOW_TIME:
            log_debug('install->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        login_cnt += 1
        log_debug('install->login', 'login_cnt=%d' % login_cnt)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        cat_num = randint(0, len(CAT) - 1)
        cat_name = CAT[cat_num]
        if RANDOM_PKG:
            pkg_num = randint(40, PKG_NUM - 1)
            package = cat_name + '_' + PKG + str(pkg_num)
        else:
            package = PACKAGE + str(PKG_START + i)
        message = json.dumps({'operator':'install', 'uid':uid, 'package':package, 'version':VERSION, 'typ':APP})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'install' != result['operator'] or uid != result['uid'] or not  result['data']:
            log_err('install', 'failed to install app %s' % str(package))
            return False
        ret = result['data']
        if not ret:
            log_err('install', 'failed to install app %s, invalid return message' % str(package))
            return False
        install_cnt += 1
        log_debug('install', 'install_cnt=%d' % install_cnt)
        if SHOW_TIME:
            log_debug('install', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        
        if SHOW_TIME:
            start_time = datetime.utcnow()
        message = json.dumps({'operator':'has_package', 'uid':uid,'package':package})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'has_package' != result['operator'] or package != result['package'] or not  result['data']:
            log_err('install-->has_package', 'failed to has app %s' % str(package))
            return False
        has_pkg_cnt += 1
        log_debug('has_package', 'has_pkg_cnt=%d' % has_pkg_cnt)
        if SHOW_TIME:
            log_debug('has_package', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        
        
        if not CATEGORIES.has_key(cat_name):
            log_err('get_top', 'failed to get the top, invalid category is %s' % str(cat_name))
            return False
        cate = CATEGORIES[cat_name]
        
        message = json.dumps({'operator':'get_top', 'category':cate})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_top' != result['operator'] or cate != result['category']:
            log_err('get_top', 'failed to get the top packages of %s' % str(cate))
            return False
        ret = result['data']
        get_top_cnt +=1
        log_debug('get_top', 'get_top_cnt=%d' % get_top_cnt)
        log_debug('get_top', 'top packages=%s' % str(ret))
        
        message = json.dumps({'operator':'get_top_details', 'category':cate})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_top_details' != result['operator'] or cate != result['category']:
            log_err('get_top_details', 'failed to get the top packages details of %s' % str(cate))
            return False
        ret = result['data']
        get_top_details_cnt += 1
        log_debug('get_top_details', 'get_top_details_cnt=%d' % get_top_details_cnt)
        log_debug('get_top_details', 'top details packages=%s' % str(ret))
        