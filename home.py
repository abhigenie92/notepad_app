#https://github.com/udacity/APIs/tree/master/Lesson_3/06_Adding%20Features%20to%20your%20Mashup/Solution%20Code
#https://www.youtube.com/playlist?list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX
#from flask import Flask,jsonify, request

from models import UsersLoginInfo,ServersAvailableInfo,Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import socket,pdb,json
from klein import run, route, Klein, resource
from os import sep

# user-defined classes
from stroke_protocol import StrokeEchoFactory
from audio_protocol import AudioEchoFactory
from twisted.internet import reactor

engine = create_engine('sqlite:///.'+sep+'database'+sep+'userslogininfo.db',\
	connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#app=Flask(__name__)
app = Klein()

#_____________________________________________________________________________________________________
@app.route('/login',methods=['POST'])
def login(request):
	'''used to allow users to login with correct corresponding password to a username'''
	data_rec = json.loads(request.content.read())
	users = [i.serialize['username'] for i in session.query(UsersLoginInfo).all()]
	passwords = [i.serialize['password'] for i in session.query(UsersLoginInfo).all()]
	login=False
	try:
		user_index=users.index(unicode(data_rec['username']))
		password_from_db=passwords[user_index]
		if password_from_db==data_rec['password']:
			login=True
			msg=None
		else:
			msg="Wrong password entered."
	except ValueError:
		msg="There is no user with that username, please create an account."
	return json.dumps({'login' : login ,"msg": msg})

#___________________________________________________________________________________________________
@app.route('/create',methods=['POST'])
def create(request):
	'''used to create users. Check if a user already exists before creating.'''
	data_rec = json.loads(request.content.read())
	users = [i.serialize['username'] for i in session.query(UsersLoginInfo).all()]
	if data_rec['username'] in users: #check account exists
		account_exists=True	
		msg="An account with that username already exists, please choose another username."
	else:
		account_exists=False
		id=len(users)
		user = UsersLoginInfo(username = unicode(data_rec['username']), 
			password = unicode(data_rec['password']), id = id)
		session.add(user)
		session.commit() 
		msg="Your account has been created. Please login with it."
	return json.dumps({'account_exists' : account_exists ,"msg": msg})
#____________________________________________________________________________________________________________
@app.route('/start_server',methods=['POST'])
def start_server(request):
	'''used to create a entry for the client ip_address & audio & stroke port. Thus, now others users can directly connect to that
	client.'''
	server_public_ip=request.client.host
	data_rec = json.loads(request.content.read())
	username=data_rec['username']
	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]
	room_exits=False 
	msg='The server has been created. Now others can connect.'
	if username in users: #check account exists
		msg='This server already existed. It has been deleted and a server has been created.'
		room_exits=True
		remove_server_from_db(data_rec['username']) # delete existing room		
	
	# code to start the server

	stroke_factory = StrokeEchoFactory(username,ServersAvailableInfo,session); 
	stroke_port_fac = reactor.listenTCP(0, stroke_factory); 
	stroke_port=stroke_port_fac.getHost().port
	stroke_factory.port = stroke_port_fac
	
	audio_factory = AudioEchoFactory(username,ServersAvailableInfo,session); 
	audio_port_fac = reactor.listenTCP(0, audio_factory); 
	audio_port=audio_port_fac.getHost().port
	audio_factory.port = audio_port_fac


	# add the entry to the rooms database
	id=len(users)
	server_room = ServersAvailableInfo(username = unicode(data_rec['username']), audio_port=audio_port,stroke_port=stroke_port, id = id)
	session.add(server_room)
	session.commit()

	return json.dumps({'room_exits' : room_exits ,"msg": msg,"stroke_port":stroke_port,"audio_port":audio_port}) 

#___________________________________________________________________________________________________________
@app.route('/connect_server',methods=['GET'])
def connect_server(request):
	'''used to retrive the client ip_address & audio & stroke port for the queried username.'''
	data_rec = json.loads(request.content.read())
	# get the entry to the room database for the user
	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]	
	ip_address='' 
	audio_port=''
	stroke_port=''
	if data_rec['server_username'] in users: #check account exists
		msg="The specified user has registered a server, establishing connection now..."
		serv_avail=True
		room_obj=session.query(ServersAvailableInfo).filter_by(username=data_rec['server_username']).one()
		audio_port=room_obj.audio_port
		stroke_port=room_obj.stroke_port
		ip_address=room_obj.ip_address
		# Here we will add the port and 
	else:
		msg="Server not available for the username you entered."
		serv_avail=False
	return json.dumps({'serv_avail':serv_avail,'msg':msg,'audio_port':audio_port,'stroke_port':stroke_port})

#_______________________________________________________________________________________________
@app.route('/delete_server',methods=['POST'])
def delete_server(request):
	'''deletes the room from base, is called on app exit'''
	data_rec = json.loads(request.content.read())
	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]
	if data_rec['username'] in users: #check account exists
		remove_server_from_db(data_rec['username'])
	return None 

def remove_server_from_db(username):
	'''removes a room from the database ServersAvailableInfo searching by argument username received
	in call'''
	room_obj=session.query(ServersAvailableInfo).filter_by(username=username).one()
	if room_obj:
		session.delete(room_obj)
		session.commit()

if __name__ == "__main__":
	app.run("localhost", 8080)
else:
	# expose a 'resource' name for use with twistd web
	resource = app.resource