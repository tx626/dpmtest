import zerorpc
from conf.dpmtest import CLI_PORT, SRV_PORT, SRV_ADDR, CLIENTS, MODE

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