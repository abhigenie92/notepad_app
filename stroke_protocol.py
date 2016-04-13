# -*- coding: utf-8 -*-
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Factory
from twisted.protocols.basic import NetstringReceiver
import json,requests,pdb
from twisted.internet import defer

class StrokeEcho(NetstringReceiver):
    def __init__(self, unregistered=True):
        self.unregistered = unregistered

    def connectionMade(self):
        print "Connected client:",self

    def stringReceived(self, string):
        payload=json.loads(string)
        operation=payload['operation']
        operation = payload['operation']
        arguments = payload['arguments']
        handlers = {
            'login': self.handle_login,
            'data': self.handle_data,
            'request_send':self.request_send,
            'allow_send': self.allow_send,
            'get_list_requests':self.get_list_requests
        }
        handler = handlers[operation]
        handler(**arguments)

    def request_send(self,message_id,stroke,audio):
        '''adds the client to the list of requested clients'''
        if self not in self.factory.requested_protocols:
            self.factory.requested_protocols[self]={'audio':audio,'stroke':stroke,'message_id':message_id}
        else:
            # what has happended: this means the client had already requested before, but he has provided a new request
            # what to do: ideally we want to update the things that false which then new message says to be true
            # 1. update msg_id
            self.factory.requested_protocols[self]['message_id']=message_id
            # 2. check if any requests have been added additionally
            ## checking for audio first
            if self.factory.requested_protocols[self]['audio']==False and audio ==True:
                self.factory.requested_protocols[self]['audio']=True
            if self.factory.requested_protocols[self]['stroke']==False and stroke ==True:
                self.factory.requested_protocols[self]['stroke']=True
        print self.username,"requested audio: %r, stroke:%r " %(audio,stroke)
        payload = {
            'operation': 'update_button_approve_request',
            'arguments': {}}
        self.factory.server_protocol.sendString(json.dumps(payload))
        # what I can do later is update on the server-client side that a request has been received

    def allow_send(self,approved_clients_stroke_usernames,approved_clients_audio_usernames):
        ''' the aim is to respond back to the clients whether their request is approved or not
            and clear
                a. the list of pending messages/requests -> requested_protocols
                Note: Each request is associated with a message on the client-side that server-client
                has not respond to yet.
                This is message on the client-side is associated with the latest callback, which when recieved:
                1. opens a popup on the client-side
                2. allows the client to send by updating the flags
        '''
        print 'The server',self.username,'approved stroke clients:',approved_clients_stroke_usernames,'audio clients:',\
            approved_clients_audio_usernames
        for protocol,value in self.factory.requested_protocols.iteritems():
            if protocol.username in approved_clients_stroke_usernames:
                # this means the client requested stroke information sending and it is approved
                status_stroke=True
            else:
                if value['stroke']==True:
                     # this means the client requested stroke information sending and it is NOT approved
                    status_stroke=False
                else:
                    # this means the client did NOT request stroke information sending 
                    status_stroke=None
            if protocol.username in approved_clients_audio_usernames:
                status_audio=True
            else:
                if value['audio']==True:
                    status_audio=False
                else:
                    status_audio=None
            payload = {
            'operation': 'approval_request',
            'arguments': {'message_id': value['message_id'],'status_stroke':status_stroke,'status_audio':status_audio}}
            protocol.sendString(json.dumps(payload))
        # set everything relating to requests as empty
        self.factory.requested_protocols={}

    def get_list_requests(self,message_id):
        audio_usernames=[protocol.username for protocol,value in self.factory.requested_protocols.iteritems() if value['audio']==True]
        stroke_usernames=[protocol.username for protocol,value in self.factory.requested_protocols.iteritems() if value['stroke']==True]
        payload = {
            'operation': 'list_of_requests',
            'arguments': {'audio_usernames': audio_usernames, 'message_id': message_id,'stroke_usernames':stroke_usernames}}
        self.sendString(json.dumps(payload))

    def handle_login(self, username):
        print username
        self.username = username
        self.unregistered = False
        if self.username==self.factory.server_username:
            self.factory.server_protocol=self

    def handle_data(self, data):
        payload = {
            'operation': 'data',
            'arguments': {'data': data}}
        for protocol in list(self.factory.protocols):
            if protocol!=self:
                protocol.sendString(json.dumps(payload))

    def connectionLost(self, reason):
        print "Client disconnected:", self.transport.getPeer(),self.username
        if self.username==self.factory.server_username: # this means the server closed down
            self.factory.disconnectAll(self)
        else:
            self.factory.disconnectOne(self)
            

class StrokeEchoFactory(Factory):
    client_requests_connection_audio={} #protocol : msg_id 
    client_requests_connection_stroke={}
    protocol = StrokeEcho
    port=''
    def __init__(self,server_username,ServersAvailableInfo,session):
        self.protocols = set()
        self.server_username = server_username
        self.closePort = Deferred()
        self.ServersAvailableInfo=ServersAvailableInfo
        self.server_protocol=''
        self.requested_protocols={} # {protocol:{audio:boolean,stroke:boolean,message_id:message_id} if no request then None  
        self.allowed_send_protcols=set()
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
