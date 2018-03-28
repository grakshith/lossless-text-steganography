import socket
import sys
import time
import threading
import select
import traceback
import struct
import time

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
            print "Waiting for files"
            filesize = clientname.recv(4)
            filesize = struct.unpack('i',filesize)[0]
            print "File Size:",filesize
            filenamesize = clientname.recv(4)
            filenamesize = struct.unpack('i',filenamesize)[0]
            print "File Name size:",filenamesize
            filename=clientname.recv(filenamesize)
            filename = filename.split('/')[1]
            chunks = filesize/4096
            print chunks
            with open('received/{}'.format(filename),'wb',4096) as f:
                chunks_written=0
                while chunks_written<chunks:
                    chunk=clientname.recv(4096)
                    f.write(chunk)
                    # print chunk
                    # chunk = clientname.recv(1024)
                    chunks_written+=1
                    print "bytes written so far = {},{}".format(chunks_written*4096,chunks_written)
                    f.flush()
                    time.sleep(0.005)
                chunk = clientname.recv(4096)
                print "Writing the last chunk"
                if(len(chunk)+chunks_written*4096>filesize):
                    chunk = chunk[:filesize- chunks_written*4096 ]
                f.write(chunk)
                f.flush()
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
