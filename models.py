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

engine = create_engine('sqlite:///var/www/FlaskApps/notepad_app/database/userslogininfo.db')
 

Base.metadata.create_all(engine)
