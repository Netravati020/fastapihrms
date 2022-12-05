from typing import Optional

from fastapi import FastAPI,  Depends, HTTPException, status
import models
import schema
import hashing
import tokn
import oauth
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
models.Base.metadata.create_all(bind=engine)
from datetime import datetime

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# craete user
@app.post('/log', tags=['login'])
def create_user(request: schema.User, db:Session=Depends(get_db)):

    new_user= models.User(user_id=request.user_id,name=request.name,email=request.email,password=hashing.Hash.encrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# user authentication
@app.post("/token", tags=['Authentication'])
async def login_access(request:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password")

    # if not hashing.Hash.verify(user.password, request.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Incorrect  password")

    access_token = tokn.create_access_token(data={"sub": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}


# delete user
@app.delete('/{user_id}', status_code=status.HTTP_200_OK, tags=['user delete'])
def delete(user_id,  db:Session=Depends(get_db)):
    u=db.query(models.User).filter(models.User.user_id == user_id).delete(synchronize_session=False)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with user_id {user_id}")

    db.commit()
    return "user deleted"

# update user details
@app.put('/{sno}', tags=['user update'])
def update(sno, request: schema.User, db:Session=Depends(get_db)):
    user =db.query(models.User).filter(models.User.sno==sno)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with user {sno}")

    user.update(dict(request))
    db.commit()

    return 'user updated'

# update user details partially
# @app.patch('/{sno}', tags=['user update'])
# def updatepartialy(sno, request: schema.newuser,db:Session=Depends(get_db)):
#     user =db.query(models.User).filter(models.User.sno==sno)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found with user {sno}")
#
#     user.update(dict(request))
#     db.commit()
#
#     return 'user updated'

# apply leave
@app.post('/',tags=['apply leave'])
def create(request: schema.Leave, db:Session=Depends(get_db),current_user: schema.User=Depends(oauth.get_current_user)):

    emp= models.Leave(employee_id=request.employee_id,name=request.name,fromdate=request.fromdate,todate=request.todate,days=request.days,leave_type=request.leave_type,reason=request.reason,status=request.status)

    db.add(emp)
    db.commit()
    db.refresh(emp)

    emp1 = models.Manager(employee_id=request.employee_id,reason=request.reason,status=request.status)
    db.add(emp1)
    db.commit()
    db.refresh(emp1)

    return "Applied for leave"


# leave approval by manager
@app.patch('/{id}', tags=['leave approval'])
def up_partially(id, request: schema.leavstatus, db:Session=Depends(get_db),current_user: schema.User=Depends(oauth.get_current_user)):
    emp =db.query(models.Leave).filter(models.Leave.id==id)
    emp1=db.query(models.Manager).filter(models.Manager.id==id)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"employee not found with id {id}")

    emp.update(dict(request))
    emp1.update(dict(request))
    db.commit()

    return 'Approved'

# read leave status
@app.get('/read', tags=['apply leave'])
def read(db:Session=Depends(get_db),current_user: schema.User=Depends(oauth.get_current_user)):
    quer= db.query(models.Leave).all()
    return quer

# employee daily punch
@app.post('/d', tags=['daily punch'])
def punch(request:schema.punch,db:Session=Depends(get_db)):
    atten = models.Dailypunch(Date=request.Date, intime=request.intime, outtime=request.outtime,attendance=request.attendance, payroll=request.payroll)
    total_time = datetime.combine(date.today(), atten.outtime) - datetime.combine(date.today(), atten.intime)
    attendance = models.Dailypunch(Date=request.Date, intime=request.intime, outtime=request.outtime,attendance=request.attendance, payroll=request.payroll, totaltime=total_time)

    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

# employee basic information
@app.post('/b', tags=['Basic info'])
def basiconfo(request:schema.basicinfo, db:Session=Depends(get_db)):
    basic_info= models.Basicinfo(branch=request.branch, department=request.department,doj=request.doj, dob=request.dob, phone=request.phone)
    db.add(basic_info)
    db.commit()
    db.refresh(basic_info)
    return basic_info

# employee task
@app.post('/t', tags=['Task assigned'])
def task(request:schema.Task,db:Session=Depends(get_db)):
    task = models.Taskassigned(meeting_name=request.meeting_name, deadline=request.deadline,priority=request.priority, update_status=request.update_status, edit_status=request.edit_status, re_assign=request.re_assign)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Dashboard
@app.get('/', tags=['Dashboard'])
def fetchdata(db:Session=Depends(get_db), current_user: schema.User=Depends(oauth.get_current_user)):

    attendance = db.query(models.Dailypunch).first()
    basic_info = db.query(models.Basicinfo).first()
    task= db.query(models.Taskassigned).first()
    leave=db.query(models.Leave).first()
    manag=db.query(models.Manager).first()

    return {"Attendance":attendance, "Basic_info":basic_info,'Task assigned':task,"Leave status":leave,"Manager":manag}

# search attendance by date
# @app.get('/date', tags=['punch'])
# def search(term: Optional[str]=None, db: Session = Depends(get_db)):
#     nam = db.query(models.Dailypunch).filter(models.Dailypunch.Date.contains(term).all())
#     attendance = []
#     for models.Dailypunch.Date in nam:
#         attendance.append(models.Dailypunch.Date)
#     return attendance
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

@app.post('/retir', tags=['Emp Retirement'])
def retir(request:schema.Retirement,db:Session=Depends(get_db)):
    emp=models.Retirement(emp_dob=request.emp_dob,date_time=request.date_time)

    age = emp.date_time.year - emp.emp_dob.year - ((emp.date_time.month, emp.date_time.day) < (emp.emp_dob.month, emp.emp_dob.day))

    mon_t=emp.date_time.month
    # time=emp.date_time.time()


    print(mon_t,type(mon_t))

    ret_age = emp.emp_dob + relativedelta(years=60)


    print(age,ret_age)

    retirement = models.Retirement(emp_dob=request.emp_dob, date_time=request.date_time,month_time=mon_t ,retirement_day=ret_age, age=age,)

    db.add(retirement)
    db.commit()
    db.refresh(retirement)
    return retirement




