# -*- coding: utf-8 -*-
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Factory
from twisted.protocols.basic import NetstringReceiver
import json,requests

class AudioEcho(NetstringReceiver):
    username=''
    def __init__(self, unregistered=True):
        self.unregistered = unregistered

    def connectionMade(self):
        print "Connected client:",self

    def dataReceived(self, data):
        if self.unregistered:
            self.unregistered=False
            recv_data=json.loads(data)
            self.username=recv_data['username']
        else:    
            for protocol in list(self.factory.protocols):
                if protocol!=self:
                    protocol.transport.write(data)

    def connectionLost(self, reason):
        print "Client disconnected:", self.transport.getPeer()
        if self.username==self.factory.server_username: # this means the server closed down
            self.factory.disconnectAll(self)
        else:
            self.factory.disconnectOne(self)
            

class AudioEchoFactory(Factory):
    protocol = AudioEcho
    port=''
    def __init__(self,server_username,ServersAvailableInfo,session):
        self.protocols = set()
        self.server_username = server_username
        self.closePort = Deferred()
        self.ServersAvailableInfo=ServersAvailableInfo
        self.session=session

    def buildProtocol(self, addr):
        protocol = Factory.buildProtocol(self, addr)
        self.protocols.add(protocol)
        return protocol

    def disconnectOne(self, non_server_protocol):
        self.protocols.remove(non_server_protocol)

    def disconnectAll(self,server_protocol):
        # remove from database
        self.remove_from_db()
        # remove all clients
        self.port.stopListening()
        
    def get_all_connected_clients(self):
        return [protocol.username for protocol in protocols if protocol.username!=self.server_username]

    def remove_from_db(self):
        users = [i.serialize['username'] for i in self.session.query(self.ServersAvailableInfo).all()]
        if self.server_username in users:
            room_obj=self.session.query(self.ServersAvailableInfo).filter_by(username=self.server_username).one()
            if room_obj:
                self.session.delete(room_obj)
                self.session.commit()

