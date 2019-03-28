import zmq
import argparse
import time
import sys
import traceback
class zreq(object):
    def __init__(self, context, address):
        self.context = context
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 1000) 
        self.address = address
        self.socket.connect(address)
        self.zpoller = zmq.Poller()
        self.zpoller.register(self.socket, zmq.POLLIN)
    
    def requestAndReply(self, outMsg, timeout):
        self.socket.send(outMsg)
        events = dict(self.zpoller.poll(timeout))
        if(self.socket in events and events[self.socket]==zmq.POLLIN):
            msg = self.socket.recv()
            return msg
        self.reset()
        return ""
    
    def reset(self):
        self.zpoller.unregister(self.socket)
        self.socket.close()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 1000) 
        self.socket.connect(self.address)
        self.zpoller.register(self.socket, zmq.POLLIN)
        
    def close(self):
        self.socket.close()
        
    def __del__(self):
        self.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="address", type=str, help='zmq request address')
    parser.add_argument('-f', dest="file", type=str, help='input file')

    args = parser.parse_args()
    fd = sys.stdin
    if(args.file):
        fd = open(args.file, 'r')
        
    zcontext = zmq.Context()
    socket = zreq(zcontext, "tcp://"+args.address)
    zpoller = zmq.Poller()
    zpoller.register(socket.socket, zmq.POLLIN)
    while(fd):
        try:
            if(fd==sys.stdin):
                outMsg = raw_input('< ')
                if(outMsg=='quit'):
                    break
            else:
                outMsg = fd.readline()
            outMsg = outMsg.strip()
            if(len(outMsg)==0):
                continue
            msg = socket.requestAndReply(outMsg, 60*1000) #timeout in 60 seconds
            if(not msg):
                print "ERROR: failed to send %s" % msg
                break;
            msg = msg.rstrip()
            print '> '+msg
        except KeyboardInterrupt:
            break
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = str(exc_value)+'\n'+('\n'.join(traceback.format_exc().splitlines()))
            print "ERROR: %s" % msg
    socket.close()   
    zcontext.term()

    
