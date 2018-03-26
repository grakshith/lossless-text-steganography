import socket
import sys
import time
import threading
import select
import traceback

class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print "Server started successfully\n"
        hostname=''
        port=51412
        self.sock.bind((hostname,port))
        self.sock.listen(5)
        print "Listening on port %d\n" %port        
        #time.sleep(2)    
        (clientname,address)=self.sock.accept()
        print "Connection from %s\n" % str(address)
        while 1:
            filename=clientname.recv(4096)
            filename = filename.split('/')[1]
            chunk=clientname.recv(4096)
            with open('received/{}'.format(filename),'wb') as f:
                f.write(chunk)
            if chunk=='':
                break
            print str(address)+':'+chunk

if __name__ == '__main__':
    srv=Server()
    srv.daemon=True
    srv.quitting=False
    print "Starting server"
    srv.start()
    time.sleep(1)
    srv.join()