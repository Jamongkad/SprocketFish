from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy.sql import text

"""
please clean this up!
"""
#try: 
#    sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db', echo=True)
#except:
#    sql_db.rollback()
#    raise
sql_db = SqlSoup('mysql://mathew:p455w0rd@localhost/hero_fish_db')
