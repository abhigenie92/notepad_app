#https://github.com/udacity/APIs/tree/master/Lesson_3/06_Adding%20Features%20to%20your%20Mashup/Solution%20Code
#https://www.youtube.com/playlist?list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX
from flask import Flask,jsonify, request
from models import UsersLoginInfo,Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///userslogininfo.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app=Flask(__name__)

@app.route('/login',methods=['POST'])
def home():
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

@app.route('/create',methods=['POST'])
def create():
	data_rec = {'username' : request.json['username'], 'password' : request.json['password']}
	users = [i.serialize['username'] for i in session.query(UsersLoginInfo).all()]
	if data_rec['username'] in users: #check account exists
		account_exists=True	
		msg="An account with that username already exists, please choose another username."
	else:
		account_exists=False
		id=len(users)
		user = UsersLoginInfo(username = unicode(data_rec['username']), password = unicode(data_rec['password']), id = id)
		session.add(user)
		session.commit() 
		msg="Your account has been created. Please login with it."
	return jsonify({'account_exists' : account_exists ,"msg": msg})

if __name__ == "__main__":
	app.run(debug="True")
