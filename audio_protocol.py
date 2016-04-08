# -*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol, Factory

class AudioEcho(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print "Connected client:",self
        self.factory.echoers.append(self)

    def dataReceived(self, data):
        for echoer in self.factory.echoers:
            if echoer!=self:
                echoer.transport.write(data)

    def connectionLost(self, reason):
        print "Audio client disconnected:",self.transport.getPeer()
        self.factory.echoers.remove(self)

class AudioEchoFactory(Factory):
    def __init__(self,server_room,server_public_ip):
        self.echoers = []
        self.server_room=server_room
        self.server_public_ip=server_public_ip

    def buildProtocol(self, addr):
        return AudioEcho(self)




