#      upload.py
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

from lib.log import log_debug, log_err
from lib.util import login, upload, DRIVER
from conf.dpmtest import  TEST_ROUNDS, SHOW_TIME, USER, USER_START, DRIVER_PACKAGE, DRIVER_START, PASSWORD, VERSION

if SHOW_TIME:
    from datetime import datetime

DRIVER_PATH = '/root/testfiles/driver'

def test():
    log_debug('upload', 'start testing ')
    login_cnt = 0
    upload_cnt = 0
    for i in range(TEST_ROUNDS):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        username = USER + str(USER_START + i)
        uid, key = login(username, PASSWORD)
        if not uid or not key:
            log_err('upload->login', 'failed to login %s.' % str(username))
            return False
        login_cnt += 1
        log_debug('upload->login', 'login_cnt=%d' % login_cnt)
        
        package = DRIVER_PACKAGE + str(DRIVER_START + i)
        if not upload(DRIVER_PATH, uid, package, VERSION, DRIVER, key):
            log_err('upload', 'failed to upload driver %s' % str(package))
            return False
        if SHOW_TIME:
            log_debug('upload', 'time=%d sec' % (datetime.utcnow() - start_time).seconds)
        upload_cnt += 1
        log_debug('upload', 'upload_cnt=%d' % upload_cnt)