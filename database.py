from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
import pymysql
from sqlalchemy.ext.declarative import declarative_base

sql_database_url= "mysql+pymysql://root@localhost:3306/htcs"
engine= create_engine(sql_database_url)
SessionLocal= sessionmaker(autocommit=False,autoflush=False, bind=engine)
conn=engine.connect()


Base= declarative_base()
print("connected")

