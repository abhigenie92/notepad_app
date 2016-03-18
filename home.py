#https://github.com/udacity/APIs/tree/master/Lesson_3/06_Adding%20Features%20to%20your%20Mashup/Solution%20Code
#https://www.youtube.com/playlist?list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX
from flask import Flask,jsonify, request
from models import UsersLoginInfo,ServersAvailableInfo,Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import socket

engine = create_engine('sqlite:///var/www/FlaskApps/notepad_app/database/userslogininfo.db',connect_args={'check_same_thread':False})
#engine = create_engine('sqlite:///./database/userslogininfo.db',connect_args={'check_same_thread':False})
available_rooms={}
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app=Flask(__name__)

#_____________________________________________________________________________________________________
@app.route('/login',methods=['POST'])
def login():
	'''used to allow users to login with correct corresponding password to a username'''

	data_rec = {'username' : request.json['username'], 'password' : request.json['password']}
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
	return jsonify({'login' : login ,"msg": msg})

#___________________________________________________________________________________________________
@app.route('/create',methods=['POST'])
def create():
	'''used to create users. Check if a user already exists before creating.'''

	data_rec = {'username' : request.json['username'], 'password' : request.json['password']}
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
	return jsonify({'account_exists' : account_exists ,"msg": msg})
#____________________________________________________________________________________________________________
@app.route('/start_server',methods=['POST'])
def start_server():
	'''used to create a entry for the client ip_address & audio & stroke port. Thus, now others users can directly connect to that
	client.'''
	data_rec = {'username':request.json['username'],'ip_address':request.json['ip_address'],'audio_port':request.json['audio_port'],
	'stroke_port' :request.json['stroke_port']}

	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]
	room_exits=False 
	msg='This server created.'
	if data_rec['username'] in users: #check account exists
		msg='This server already existed. It has been deleted and a server has been created.'
		room_exits=True
		remove_server_from_db(data_rec['username']) # delete existing room		
	# add the entry to the rooms database
	id=len(users)
	server_room = ServersAvailableInfo(username = unicode(data_rec['username']), ip_address=unicode(data_rec['ip_address'])
              ,audio_port=request.json['audio_port'],stroke_port=request.json['stroke_port'], id = id)
	session.add(server_room)
	session.commit()
	return jsonify({'room_exits' : room_exits ,"msg": msg}) 

#___________________________________________________________________________________________________________
@app.route('/connect_server',methods=['GET'])
def connect_server():
	'''used to retrive the client ip_address & audio & stroke port for the queried username.'''
	data_rec = {'server_username' : request.json['server_username']}	
	# get the entry to the room database for the user
	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]	
	ip_address='' 
	audio_port=''
	stroke_port=''
	if data_rec['server_username'] in users: #check account exists
		msg="Server available, establishing connection now."
		serv_avail=True
		room_obj=session.query(ServersAvailableInfo).filter_by(username=server_username).one()
		print room_obj
	
	else:
		msg="Server not available for the username you entered."
		serv_avail=False

#_______________________________________________________________________________________________
@app.route('/delete_server',methods=['POST'])
def delete_server():
	'''deletes the room from base, is called on app exit'''
	data_rec = {'username':request.json['username']}
	users = [i.serialize['username'] for i in session.query(ServersAvailableInfo).all()]
	if data_rec['username'] in users: #check account exists
		remove_server_from_db(data_rec['username'])
	return None 

def remove_server_from_db(username):
	'''removes a room from the database ServersAvailableInfo searching by argument username received
	in call'''
	room_obj=session.query(ServersAvailableInfo).filter_by(name=username).one()
	if room_obj:
		session.delete(room_obj)
		session.commit()

if __name__ == "__main__":
	app.run(debug="True")
