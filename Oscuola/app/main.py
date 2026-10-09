import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi import Depends
from database.fetch import check_login,get_grades,get_class_grades,get_alerts_1st,timetable,get_classes,get_reqs,getstudents,test,report_ts,load_reps,get_repcontent,lspci
from database.insert import insert_request,postit,accept_it,delete_it,modifygrades
from pydantic import BaseModel
class LoginRequest(BaseModel):
    gmail: str
    passwd: str
class reportsss(BaseModel):
    classs : str
    id : int

class reportsssteach(BaseModel):
    classs : str
    id : int
    teach_id: int






class classs(BaseModel):
    classs : int
    year : int
class classsstr(BaseModel):
    classs : str


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


class repinfo(BaseModel):
    name : str
    classs : str



class grades1st(BaseModel):
    id : int
    mathematics : float
    french : float
    english : float
    cs : float
    physics : float
    sc : float


app = FastAPI()
from fastapi import Header, HTTPException
def verify_key(authorization: str = Header(None)):
    if authorization != f"Bearer {os.environ['API_KEY']}":
        raise HTTPException(status_code=401, detail="Unauthorized ass bitch")
@app.get("/")
def root():
    return {"message": "online"}




@app.post("/load_reports")
def lorep(data : ids, authorized: None = Depends(verify_key)):
    return load_reps(data.id)



@app.get("/test")
def tests():
    test()
    return {"message": "done"}

@app.post("/generate_rep")
def tap(data : reportsssteach,authorized: None = Depends(verify_key)):
    return report_ts(data.classs,data.id,data.teach_id)




@app.post("/rap_content")
def tap(data : repinfo,authorized: None = Depends(verify_key)):
    return get_repcontent(data.name,data.classs)












@app.get("/list_classes")
def lc(authorized: None = Depends(verify_key)):
    return lspci()





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


@app.post("/get_grades")
def syst(data : ids, authorized: None = Depends(verify_key)):
    return get_grades(data.id)


@app.post("/get_class_grades")
def gcg(data : classsstr, authorized: None = Depends(verify_key)):
    return get_class_grades(data.classs)



@app.post("/change_grades")
def cg1(data : grades1st,authorized: None = Depends(verify_key)):
    return modifygrades(data)


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

@app.post("/get_students")
def gs(data : classsstr,authorized: None = Depends(verify_key)):
    return getstudents(int(data.classs[0]),int(data.classs[2]))








