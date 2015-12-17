import os
import fcntl
import struct
import socket
import types
import hashlib
from lib.zip import zip_dir
from random import randint
from log import log_debug, log_err
from component.rpcclient import RPCClient
from conf.dpmtest import MANAGER_PORTS, MANAGER_SERVERS, FRONTEND_SERVERS, FRONTEND_PORT, IFACE

APP = 'app'

def get_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return  socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', IFACE[:15]))[20:24])

def get_frontend():
    n = randint(0, len(FRONTEND_SERVERS) - 1)
    return FRONTEND_SERVERS[n]

def get_manager():
        n = randint(0, len(MANAGER_SERVERS) - 1)
        server =  MANAGER_SERVERS[n]
        #log_debug('util', 'manager=%s' % str(server))
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
    zipfilename = '%s-%s.zip' % (package, version)
    zipfilepath = os.path.join('/tmp', zipfilename)
    zip_dir(path, zipfilepath)
    with open(zipfilepath) as f:
        buf = f.read()
    os.remove(zipfilepath)
    addr = get_frontend()
    rpcclient = RPCClient(addr, FRONTEND_PORT, uid, key)
    ret  = rpcclient.request('upload', uid=uid, package=package, version=version, buf=buf, typ=typ)
    if ret:
        #log_debug('util', "finished uploading, package=%s, version=%s, ret=%s" % (package, version, str(ret)))
        return True
    else:
        log_err('util', 'failed to upload, uid=%s, package=%s, version=%s, typ=%s' % (str(uid), str(package), str(version), str(typ)))
        return False
