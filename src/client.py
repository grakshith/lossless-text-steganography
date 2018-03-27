import socket
import sys
import time
import threading
import os
from ctypes import c_int32

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))
    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        # print "Sent\n"
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            host=raw_input("Enter the hostname\n>>")            
            port=int(raw_input("Enter the port\n>>"))
        except EOFError:
            print "Error"
            return 1
        
        # print "Connecting\n"
        s=''
        self.connect(host,port)
        # print "Connected\n"
        while 1:            
            print "Enter filename:\n"
            filename=raw_input('>>')
            if filename=='exit':
                break
            if filename=='':
                continue
            print "Sending file {}\n".format(filename)
            filesize = os.path.getsize(filename)
            filesize = c_int32(filesize)
            self.client(host,port,filesize)
            filenamesize = c_int32(len(filename))
            self.client(host,port,filenamesize)
            self.client(host,port,filename)
            with open(filename, 'rb') as f:
                chunk = f.read(1024)
                while chunk:
                    self.client(host,port,chunk)
                    chunk = f.read(1024)
            print "Sent\n"
        return(1)

if __name__=='__main__':
    print "Starting client"
    cli=Client()
    print "Started successfully"
    cli.start()
    cli.join()
