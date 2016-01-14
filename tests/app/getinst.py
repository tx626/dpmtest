#      getinst.py
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
from lib.util import get_manager, get_port
from websocket import create_connection
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, PKG_START, PACKAGE

if SHOW_TIME:
    from datetime import datetime

PKG = 'pkg'
PKG_NUM = 200
CAT = ['cat0', 'cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7']
RANDOM_PKG = True

def test():
    log_debug('get_description', 'start testing ')
    get_inst_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_PKG:
            cat_num = randint(0, len(CAT) - 1)
            cat_name = CAT[cat_num]
            pkg_num = randint(0, PKG_NUM - 1)
            package = cat_name + '_' + PKG + str(pkg_num)
        else:
            package = PACKAGE + str(PKG_START + i)
        
        message = json.dumps({'operator':'get_inst', 'package':package})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_inst' != result['operator'] or package != result['package']:
            log_err('get_description', 'failed to get the valid message' )
            return False
        get_inst_cnt += 1
        log_debug('get_inst', 'get_inst_cnt=%d' % get_inst_cnt)
        log_debug('get_inst', 'the number of %s has been installed is %s' % (str(package), str(result['data'])))
        if SHOW_TIME:
            log_debug('get_inst', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
