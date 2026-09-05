import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi import Depends
from database.fetch import test,check_login
from database.insert import insert_request
from pydantic import BaseModel
class LoginRequest(BaseModel):
    gmail: str
    passwd: str
class insert_Request(BaseModel):
    gmail: str
    passwd: str
app = FastAPI()
from fastapi import Header, HTTPException
def verify_key(authorization: str = Header(None)):
    if authorization != f"Bearer {os.environ['API_KEY']}":
        raise HTTPException(status_code=401, detail="Unauthorized ass bitch")
@app.get("/")
def root():
    s = test()
    return {"message": s}

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
    if result =="pass":
        return {"message": "pass"}

    return {"message": result}


@app.post("/insert_request")
def insert(data: insert_Request, authorized: None = Depends(verify_key)):
    result = insert_request(data.gmail, data.passwd)
    if result == True:
        return {"message": "inserted"}

    return {"message": result}
