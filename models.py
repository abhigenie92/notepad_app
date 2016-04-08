# -*- coding: utf-8 -*-
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from os import pathsep

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
      'audio_port': self.audio_port,
      'stroke_port': self.stroke_port,
      }

engine = create_engine('sqlite:///.'+pathsep+'database'+pathsep+'userslogininfo.db')
  

Base.metadata.create_all(engine)
