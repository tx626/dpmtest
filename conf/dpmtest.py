from lib.mode  import TEST_REGISTER
MODE = TEST_REGISTER

PKG_NUM = 160
PKG_START = 0
USER_START = 0

FRONTEND_PORT = 9001
FRONTEND_SERVERS = ['192.168.10.128', '192.168.10.129', '192.168.10.130', '192.168.10.131']

CLI_PORT = 4342
SRV_PORT = 4343
TEST_ROUNDS = 10000
MANAGER_PORTS = [i for i in range(10001, 10002)]
MANAGER_SERVERS = ['192.168.10.197', '192.168.10.12', '192.168.10.13', '192.168.10.14']
SRV_ADDR = '192.168.10.36'

CLIENTS = 16
IFACE = 'eth0'

USER = 'user4'
VERSION = '0.0.1'
CATEGORY = '0'
PACKAGE = 'pkgapp1'
PASSWORD = '123456'
EMAIL = 'user@gmail.com'

LOG_ERROR = True
LOG_DEBUG = True
SHOW_TIME = True
