import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from database.fetch import test,check_login
app = FastAPI()
from fastapi import Header, HTTPException
def verify_key(authorization: str = Header(None)):
    if authorization != f"Bearer {os.environ['auth_key']}":
        raise HTTPException(status_code=401, detail="Unauthorized ass bitch")
@app.get("/")
def root():
    s = test()
    return {"message": s}

@app.post("/login_check")
def check(data):
    verify_key()
    if(check_login(data.gmail,data.password)=="pass"):
        return {"message": "pass"}
    else:
        return {"message": "not found"}


