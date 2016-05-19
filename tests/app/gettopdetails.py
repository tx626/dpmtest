#      gettopdetails.py
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
from lib.util import get_manager, get_port
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, CATEGORY

if SHOW_TIME:
    from datetime import datetime

CAT = ['cat0]
RANDOM_CAT = True

def test():
    log_debug('register', 'start testing ')
    get_top_details_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        
        if RANDOM_CAT:
            cat_num = randint(0, len(CAT) - 1)
            cat_name = CAT[cat_num]
            if not CATEGORIES.has_key(cat_name):
                log_err('get_top_details', 'failed to get the top details, invalid category is %s' % str(cat_name))
                return False
            cate = CATEGORIES[cat_name]
        else:
            cate = CATEGORY
        
        message = json.dumps({'operator':'get_top_details', 'category':cate})
        ws = create_connection("ws://%s:%d/" % (get_manager(), get_port()))
        ws.send(message)
        ret = ws.recv()
        ws.close()
        result = json.loads(ret)
        if not result or 'get_top_details' != result['operator'] or cate != result['category']:
            log_err('get_top_details', 'failed to get the top packages details of %s' % str(cate))
            return False
        if SHOW_TIME:
            log_debug('register', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        ret = result['data']
        get_top_details_cnt += 1
        log_debug('get_top_details', 'get_top_details_cnt=%d' % get_top_details_cnt)
        log_debug('get_top_details', 'top details packages=%s' % str(ret))