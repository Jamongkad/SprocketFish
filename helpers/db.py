from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.sqlsoup import SqlSoup

import hashlib

mysql_db = create_engine('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id       = Column(Integer(11), primary_key=True)
    name     = Column(String(50))
    fullname = Column(String(125))
    password = Column(String(64))

    def __init__(self, name, fullname, password):
        self.name     = name
        self.fullname = fullname
        self.password = hashlib.sha1(password).hexdigest()

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

class Job(Base):

    __tablename__ = 'jobs'
    job_id   = Column(Integer(10), primary_key=True)
    job_nm   = Column(String(100))
    job_desc = Column(Text())

    def __init__(self, job_nm, job_desc):
        self.job_nm   = job_nm
        self.job_desc = job_desc

    def __repr__(self):
        return "<Job('%s', '%s')>" % (self.job_nm, self.job_desc)

metadata = Base.metadata
metadata.create_all(mysql_db)

Session = sessionmaker(bind=mysql_db)
session = Session()

"""
please clean this up!
"""
try: 
    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)
except:
    sql_db.rollback()
    raise
