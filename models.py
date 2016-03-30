# -*- coding: utf-8 -*-
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
class UsersLoginInfo(Base):
  __tablename__ = 'userslogininfo'
  id = Column(Integer, primary_key = True)
  username = Column(String)
  password = Column(String)  
  
  #Add a property decorator to serialize information from this database
  @property
  def serialize(self):
    return {
      'username': self.username,
      'password': self.password,
      }
class ServersAvailableInfo(Base):
  __tablename__ = 'serversavailable'
  id = Column(Integer, primary_key = True)
  username = Column(String)
  ip_address = Column(String)
  audio_port= Column(Integer)
  stroke_port= Column(Integer)
  #Add a property decorator to serialize information from this database
  @property
  def serialize(self):
    return {
      'username': self.username,
      'ip_address': self.ip_address,
      'audio_port': self.audio_port,
      'stroke_port': self.stroke_port,
      }

engine = create_engine('sqlite:///var/www/FlaskApps/notepad_app/database/userslogininfo.db')
#engine = create_engine('sqlite:///./database/userslogininfo.db')
  

Base.metadata.create_all(engine)
