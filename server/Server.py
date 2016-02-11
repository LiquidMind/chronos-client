import threading

from time import gmtime, strftime

from server.JSONSocket import Server
import time


class ServerSide:
    def __init__(self):
        print 'runServerSide'
        self.is_accepted = False
        t = threading.Thread(target=self.initServerHook)
        t.daemon = False
        t.start()
        self.server = None

    def isAccepted(self):
        return self.is_accepted

    def initServerHook(self):
        print 'init server'
        self.server = Server('127.0.0.1', 27555)
        print "in accept lock"
        self.server.accept()
        self.is_accepted = True

    def send(self, json):
        print "send %s" % json
        self.server.send(json)


phases = {}
