#      util.py
#      
#      Copyright (C) 2015  Xu Tian <tianxu@iscas.ac.cn>
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

import os
import fcntl
import struct
import socket
import types
import shutil
import hashlib
import tempfile
import commands
from random import randint
from log import log_debug, log_err
from lib.zip import zip_dir, unzip_file
from conf.path import PATH_DRIVER 
from component.rpcclient import RPCClient
from conf.servers import SERVER_FRONTEND, SERVER_MANAGER
from conf.dpmtest import MANAGER_PORTS, FRONTEND_PORT, IFACE

APP = 'app'
DRIVER = 'driver'

def get_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return  socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', IFACE[:15]))[20:24])

def get_frontend():
    n = randint(0, len(SERVER_FRONTEND) - 1)
    return SERVER_FRONTEND[n]

def get_manager():
    n = randint(0, len(SERVER_MANAGER) - 1)
    server =  SERVER_MANAGER[n]
    return server

def get_port():
    n = randint(0, len(MANAGER_PORTS) - 1)
    return MANAGER_PORTS[n]

def get_md5(text):
    if type(text) is types.StringType:
        tmp = hashlib.md5()   
        tmp.update(text)
        return tmp.hexdigest()
    else:
        log_err('util', 'failed to get md5')

def login(user, password):
    user = str(user)
    pwd = get_md5(str(password))
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT)
    uid, key = rpcclient.request('login', user=user, pwd=pwd)
    return (str(uid), str(key))

def upload(path, uid, package, version, typ, key):
    zipfilename = '%s-%s.zip' % (str(package), str(version))
    zipfilepath = os.path.join('/tmp', zipfilename)
    zip_dir(path, zipfilepath)
    with open(zipfilepath) as f:
        buf = f.read()
    os.remove(zipfilepath)
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT, uid, key)
    ret  = rpcclient.request('upload', uid=uid, package=package, version=version, buf=buf, typ=typ)
    if ret:
        return True
    else:
        log_err('util', 'failed to upload, uid=%s, package=%s, version=%s, typ=%s' % (str(uid), str(package), str(version), str(typ)))
        return False

def install(uid, package, version, typ):
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT)
    ret = rpcclient.request('install', uid=uid, package=package, version=version, typ=typ)
    if not ret:
        log_err('util', 'failed to install, uid=%s, package=%s, version=%s, typ=%s' % (str(uid), str(package), str(version), str(typ)))
        return
    return ret

def install_driver(uid, package, version=None):
    driver_path = os.path.join(PATH_DRIVER, package)
    if os.path.exists(driver_path):
        shutil.rmtree(driver_path)
    ret = install(uid, package, version, DRIVER)
    if not ret:
        log_err('util', 'failed to install driver, uid=%s, driver=%s, version=%s' % (str(uid), str(package), str(version)))
        return False
    dirname = tempfile.mkdtemp()
    try:
        src = os.path.join(dirname, package) + '.zip'
        with open(src, 'wb') as f:
            f.write(ret)
        dest = os.path.join(dirname, package)
        unzip_file(src, dest)
        dep_path = os.path.join(dest, 'dep')
        if not _check_dep(dep_path):
            log_err('util', 'failed to install driver, invalid dependency, uid=%s, driver=%s, version=%s' % (str(uid), str(package), str(version)))
            return False
        os.remove(dep_path)
        shutil.copytree(dest, driver_path)
    finally:
        shutil.rmtree(dirname)
    return True

def _check_dep(path):
    if os.path.exists(path):
        with open(path) as file_dependency:
            lines = file_dependency.readlines()
            for line in lines:
                try:
                    package_version = ''
                    installer_name = ''
                    res = []
                    
                    for str_equal in line.split('='):
                        if str_equal.strip(): # not blank
                            for str_blank in str_equal.split():
                                res.append(str_blank)
                    
                    if len(res) % 2 == 0:
                        if len(res):
                            log_err('util', 'failed to check dependency, invalid format' )
                            return False
                        continue # if it is blank, then continue
                    else:
                        package_name =  res[0]
                        
                        for index_to_match in range(1, len(res), 2):
                            if res[index_to_match] == 'installer':
                                installer_name = res[index_to_match + 1]
                                continue
                            if res[index_to_match] == 'version':
                                package_version = res[index_to_match + 1]
                                continue
                        
                        if installer_name == '':
                            installers = ['pip', 'apt-get']
                            for installer in installers:
                                installer_name = installer
                                if package_version == '': 
                                    cmd = '%s install %s' % (str(installer_name), str(package_name))
                                else :
                                    cmd = '%s install %s==%s' % (str(installer_name), str(package_name), str(package_version))
                                status, output = commands.getstatusoutput(cmd)
                                if status == 0:
                                    log_debug('util', 'check dependency, finished installing %s' % str(package_name))
                                    break
                            if status != 0:
                                log_err('util', 'check dependency, invalid installer, failed to install %s' % str(package_name))
                                return False
                        else:
                            if package_version == '':
                                cmd = '%s install %s' % (str(installer_name), str(package_name))
                            else:
                                cmd = '%s install %s==%s' % (str(installer_name), str(package_name), str(package_version))
                            status, output = commands.getstatusoutput(cmd)
                            if status == 0:
                                log_debug('util', 'check dependency, finished installing %s' % str(package_name))
                            else:
                                log_err('util', 'check dependency, failed to install %s' % str(package_name))
                                return False
                except:
                    continue # if it is blank, continue. else return False
        return True
