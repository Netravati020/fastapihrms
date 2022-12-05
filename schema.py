
from datetime import datetime, date, time
from pydantic import BaseModel
from sqlalchemy import DateTime
from typing import Optional



class User(BaseModel):

    user_id:Optional[str]
    name:Optional[str]
    password:Optional[str]
    email:Optional[str]


class Login(BaseModel):
    purchase_id: str
    password:str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    purchase_id: str

    class Config:
        orm_mode = True

class newuser(BaseModel):

    name:str

    class Config:
        orm_mode = True
class leavstatus(BaseModel):

    status:str

    class Config:
        orm_mode = True

class Leave(BaseModel):
    employee_id :str
    name :Optional[str]
    fromdate :Optional[date]
    todate :Optional[date]
    days :Optional[int]
    leave_type:Optional[str]
    reason :str
    status:str

    class Config:
        arbitrary_types_allowed = True

class punch(BaseModel):

    Date :Optional[date]
    intime :Optional[time]
    outtime :Optional[time]
    totaltime:Optional[time]
    attendance :Optional[str]
    payroll :Optional[str]

    class Config:
        orm_mode = True

class basicinfo(BaseModel):
    branch: Optional[str]
    department: Optional[str]
    doj: Optional[str]
    dob: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True

class Task(BaseModel):
    meeting_name: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]
    update_status: Optional[str]
    edit_status: Optional[str]
    re_assign: Optional[str]

    class Config:
        orm_mode = True

class Retirement(BaseModel):
    emp_dob : Optional[date]
    age:Optional[int]
    date_time :Optional[datetime]

    month_time :Optional[int]

    retirement_day :Optional[date]

