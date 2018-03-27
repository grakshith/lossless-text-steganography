import socket
import sys
import time
import threading
import select
import traceback
import struct

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
        try:
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
                data_read=1024
                chunks = filesize/1024
                with open('pickled/{}'.format(filename),'wb',1024) as f:
                    chunks_written=0
                    while chunks_written<chunks:
                        chunk=clientname.recv(1024)
                        f.write(chunk)
                        # print chunk
                        # chunk = clientname.recv(1024)
                        chunks_written+=1
                    chunk = clientname.recv(filesize%1024)
                    f.write(chunk)
                    f.flush()
                if chunk=='':
                    break
                print str(address)+':'+chunk
        except Exception as e:
            raise e
        finally:
            clientname.close()

if __name__ == '__main__':
    srv=Server()
    srv.daemon=True
    srv.quitting=False
    print "Starting server"
    srv.start()
    time.sleep(1)
    srv.join()
