import socket
import asyncore
import time

class http_server(asyncore.dispatcher):

    def __init__(self, ip, port):
        print "init http_server"
        self.ip= ip
        self.port = port
        self.count = 0
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ip, port))
        self.listen(5)

    def writable(self):
        #print "server: not writable"
        return 0

    def handle_read(self):
        #print "server: handle_read"
        pass

    def readable(self):
        #print "server: not readable"
        return self.accepting

    def handle_connect(self):
        #print "server: connect"
        pass

    def handle_accept(self):
        #print "server: accept"
        try:
            conn, addr = self.accept()
        except socket.error: # rare Linux error
            print "Socket error on server accept()"
            return
        except TypeError: # rare FreeBSD3 error
            print "EWOULDBLOCK exception on server accept()"
            return
        self.count += 1
        handler = http_handler(conn, addr, self, self.count)

    def decrement(self):
        #print "server: decrement"
        self.count -= 1

class http_handler(asyncore.dispatcher):

    def __init__(self, conn, addr, server, count):
        print "init http_handler", count
        asyncore.dispatcher.__init__(self, sock=conn)
        self.addr = addr
        self.buffer = ""
        self.time = time.time()
        self.count = count
        self.server = server

    def handle_read(self):
        print "handler: read", self.count
        rq = self.recv(1024)
        self.buffer = """HTTP/1.0 200 OK Canned Response Follows
Content-Type: text/html

<HTML>
<HEAD>
    <TITLE>Response from server</TITLE>
</HEAD>
<BODY>
<P>This is socket number %d
</BODY>
""" % self.count

    def writable(self):
        print "handler: writable", self.count
        if time.time()-self.time > 10:
            rc = len(self.buffer) > 0
        else:
            rc = 0
        print "handler: writable returning", rc
        return rc

    def handle_write(self):
        print "handler: handle_write", self.count
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        if len(self.buffer) == 0:
            print "handler: closing", self.count
            self.close()
        self.server.decrement()

server = http_server('', 8080)

asyncore.loop(timeout=4.0)

