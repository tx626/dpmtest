import zerorpc
import resource
from lib import mode
from lib.util import get_addr
from threading import Thread
from conf.dpmtest import CLI_PORT, SRV_PORT, SRV_ADDR

def start_client():
    cli = zerorpc.Client()
    cli.connect('tcp://%s:%d' % (SRV_ADDR, SRV_PORT))
    cli.join(get_addr())
    cli.close()

class Listener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.mode = None
    
    def start_test(self, name):
        self.mode = name
        self.start()
    
    def run(self):
        if self.mode == mode.TEST_REGISTER:
            from tests.websocket import generator
            generator.test()

if __name__ == '__main__':
    max_open_files_soft, max_open_files_hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (4096, max_open_files_hard))
    s = zerorpc.Server(Listener())
    Thread(target=start_client).start()
    print 'client--addr', get_addr()
    s.bind("tcp://%s:%d" % (get_addr(), CLI_PORT))
    s.run()
