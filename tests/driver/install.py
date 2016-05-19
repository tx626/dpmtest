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

from random import randint
from lib.log import log_debug, log_err
from lib.util import login, install_driver
from conf.dpmtest import TEST_ROUNDS, SHOW_TIME, USER, USER_START, DRIVER_PACKAGE, DRIVER_START, PASSWORD, VERSION, DRIVER_NUM

if SHOW_TIME:
    from datetime import datetime

RANDOM_DRIVER = True

def test():
    log_debug('install', 'start testing ')
    login_cnt = 0
    install_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        uid, key = login(username, PASSWORD)
        if not uid or not key:
            log_err('install->login', 'failed to login %s.' % str(username))
            return False
        login_cnt += 1
        log_debug('install->login', 'login_cnt=%d' % login_cnt)
        if SHOW_TIME:
            log_debug('install->login', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
            start_time = datetime.utcnow()
        
        if RANDOM_DRIVER:
            driver_num = randint(40, DRIVER_NUM - 1)
            package = DRIVER_PACKAGE + str(driver_num)
        else:
            package = DRIVER_PACKAGE + str(DRIVER_START + i)
        
        if not install_driver(uid, package, VERSION):
            log_err('instll', 'failed to install driver %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('install', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        install_cnt += 1
        log_debug('install', 'install_cnt=%d' % install_cnt)