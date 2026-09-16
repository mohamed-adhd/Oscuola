import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi import Depends
from database.fetch import test,check_login,get_grades_1st,get_alerts_1st,timetable,get_classes,get_reqs
from database.insert import insert_request,postit,accept_it,delete_it
from pydantic import BaseModel
class LoginRequest(BaseModel):
    gmail: str
    passwd: str

class registerRequest(BaseModel):
    gmail: str
    passwd: str
    classs : str
    name : str
    aftername : str

class insert_Request(BaseModel):
    gmail: str
    passwd: str
    classs: str
class tb_Request(BaseModel):
    classs: int
    year: int
class ids(BaseModel):
    id : int

class post_request(BaseModel):
    subject: str
    message: str

class req(BaseModel):
    name : str
    aftername : str
    classs : str




app = FastAPI()
from fastapi import Header, HTTPException
def verify_key(authorization: str = Header(None)):
    if authorization != f"Bearer {os.environ['API_KEY']}":
        raise HTTPException(status_code=401, detail="Unauthorized ass bitch")
@app.get("/")
def root():
    return {"message": "online"}

@app.get("/debug-key")
def debug_key(authorization: str = Header(None)):
    expected = f"Bearer {os.environ['API_KEY']}"

    print("RECEIVED:", repr(authorization))
    print("EXPECTED:", repr(expected))
    print("RECEIVED LENGTH:", len(authorization) if authorization else None)
    print("EXPECTED LENGTH:", len(expected))
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized my guy")
    return None


@app.post("/login_check")
def check(data: LoginRequest, authorized: None = Depends(verify_key)):
    result = check_login(data.gmail, data.passwd)
    if isinstance(result, dict):
        return result
    return {"message": result}

#this shi aint fun no more twin
@app.post("/insert_register")
def insert(data: registerRequest, authorized: None = Depends(verify_key)):
    result = insert_request(data.gmail, data.passwd,data.classs,data.name,data.aftername)
    if result == True:
        return {"message": "inserted"}
    return {"message": result}


@app.post("/s1t_year_student")
def syst(data : ids, authorized: None = Depends(verify_key)):
    return get_grades_1st(data.id)
#testing 
@app.get("/pfp")
def insrtpfp():
    return test()
@app.get("/__routes")
def list_routes():
    return [r.path for r in app.routes]


@app.post("/s1t_alerts")
def sysa(data : ids, authorized: None = Depends(verify_key)):
    return get_alerts_1st(data.id)

@app.post("/timetable")
def sysb(data : tb_Request, authorized: None = Depends(verify_key)):
    return timetable(data.classs,data.year)

@app.post("/get_myclasses")
def gmc(data : ids, authorized: None = Depends(verify_key)):
    return get_classes(data.id)


@app.post("/get_requests")
def grq(data : ids, authorized: None = Depends(verify_key)):
    return get_reqs(data.id)



@app.post("/accept_request")
def acr(data : req, authorized: None = Depends(verify_key)):
    return accept_it(data.classs,data.name,data.aftername)

@app.post("/delete_request")
def der(data : req, authorized: None = Depends(verify_key)):
    return delete_it(data.classs,data.name,data.aftername)


@app.post("/post_request")
def pst(data : post_request, authorized: None = Depends(verify_key)):
    return postit(data.subject,data.message)