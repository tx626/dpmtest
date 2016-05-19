#      coordinator.py
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

import zerorpc
from conf.servers import SRV_ADDR
from conf.dpmtest import CLI_PORT, SRV_PORT, CLIENTS, MODE

class Coordinator(object):
    def __init__(self):
        self._cnt = 0
        self._addr = []
        
    def join(self, addr):
        self._cnt += 1
        self._addr.append(addr)
        print 'server 4-1', self._addr
        if self._cnt == CLIENTS:
            for i in self._addr:
                print 'server 4-2', i
                cli = zerorpc.Client()
                cli.connect('tcp://%s:%d' % (i, CLI_PORT))
                print 'server 4-3'
                cli.start_test(MODE)

if __name__ == '__main__':
    s = zerorpc.Server(Coordinator())
    s.bind("tcp://%s:%d" % (SRV_ADDR, SRV_PORT))
    s.run()