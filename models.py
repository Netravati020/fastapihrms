from datetime import time

from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, table, DateTime, Time, BigInteger
from sqlalchemy.orm import relationship


# user table
class User(Base):
    __tablename__='loginuser'
    sno=Column(Integer,primary_key=True, autoincrement=True)
    user_id=Column(String(100),index=True)
    name=Column(String(50), index=True)
    password=Column(String(100),index=True)
    email=Column(String(50),index=True)

class Leave(Base):
    __tablename__='leaves'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    employee_id = Column(String(100), unique=True, index=True)
    name = Column(String(100), index=True)
    fromdate = Column(Date, index=True)
    todate = Column(Date, index=True)
    days = Column(Integer, index=True)
    leave_type= Column(String(100), index=True)
    reason = Column(String(200), index=True)
    status= Column(String(50), index=True)
    # items = relationship("Aproval", back_populates="owner")

class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    employee_id = Column(String(100), unique=True, index=True)
    reason = Column(String(200), index=True)
    status = Column(String(50), index=True)

    # l_id = Column(Integer, ForeignKey("leaves.id"), nullable=False)
    #
    # owner = relationship("Leave", back_populates="items")



class Dailypunch(Base):
    __tablename__='dailypunch'

    sno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Date = Column(Date, index=True)
    intime = Column(Time, index=True)
    outtime = Column(Time, index=True)
    totaltime = Column(Time, index=True)
    attendance = Column(String(50), index=True)
    payroll = Column(String(50), index=True)

class Basicinfo(Base):
    __tablename__='basicinfo'
    emp_id=Column(Integer,primary_key=True,autoincrement=True, index=True)
    branch= Column(String(50), index=True)
    department=Column(String(50), index=True)
    doj= Column(String(50),index=True)
    dob=Column(String(50), index=True)
    phone=Column(BigInteger, index=True)

class Taskassigned(Base):
    __tablename__='task_assigned'

    sno=Column(Integer,primary_key=True, autoincrement=True, index=True)
    meeting_name= Column(String(50), index=True)
    deadline= Column(String(50), index=True)
    priority= Column(String(50), index=True)
    update_status= Column(String(50), index=True)
    edit_status= Column(String(50),index=True)
    re_assign=Column(String(50),index=True)

class Retirement(Base):
    __tablename__='retirement'
    sno=Column(Integer,primary_key=True, autoincrement=True, index=True)
    emp_dob= Column(Date, index=True)
    age= Column(Integer, index=True)
    date_time= Column(DateTime, index=True)

    month_time=Column(Integer, index=True)
    retirement_day=Column(Date, index=True)





