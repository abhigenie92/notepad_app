# -*- coding: utf-8 -*-
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Factory
from twisted.protocols.basic import NetstringReceiver
import json,requests
class StrokeEcho(NetstringReceiver):
    def __init__(self, unregistered=True):
        self.unregistered = unregistered

    def connectionMade(self):
        print "Connected client:",self

    def stringReceived(self, string):
        if self.unregistered:
            self.username=json.loads(string)
            self.unregistered=False

            if self.username==self.factory.server_username:
                self.factory.rooms[self.factory.server_username].server_protocol_stroke=self
                self.factory.rooms[self.factory.server_username].connected_protocols_stroke.add(self)
            else:
                self.factory.rooms[self.factory.server_username].connected_protocols_stroke.add(self)
        else:
            for protocol in self.factory.rooms[self.factory.server_username].connected_protocols_stroke:
                if protocol!=self:
                    protocol.sendString(string)

    def connectionLost(self, reason):
        print "Client disconnected:", self.transport.getPeer()
        if self.username==self.factory.server_username: # this means the server closed down
            self.factory.disconnectAll(self)
        else:
            self.factory.disconnectOne(self)
            

class StrokeEchoFactory(Factory):
    protocol = StrokeEcho
    def __init__(self,server_username,rooms):
        self.protocols = set()
        self.echoers = []
        self.server_username = server_username
        self.closePort = Deferred()
        self.rooms=rooms

    def buildProtocol(self, addr):
        protocol = Factory.buildProtocol(self, addr)
        self.protocols.add(protocol)
        return protocol

    def disconnectOne(self, non_server_protocol):
        self.protocols.remove(non_server_protocol)

    def disconnectAll(self,server_protocol):
        # delete from room dictionary
        if self.rooms[self.server_username]:
            del self.rooms[self.server_username]
        # remove from database
        requests.post('http://127.0.0.1:8080'+"/delete_server", json={'username':self.username})
        # remove all clients
        self.stopListening()
        
    def get_all_connected_clients(self):
        return [protocol.username for protocol in protocols if protocol.username!=self.server_username]
