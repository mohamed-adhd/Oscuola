import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from fastapi import Depends
from database.fetch import test,check_login
from pydantic import BaseModel
class LoginRequest(BaseModel):
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
def debug_key():
    return {"key_length": len(os.environ.get("API_KEY", "MISSING")), "starts_with": os.environ.get("API_KEY", "")[:4]}
@app.post("/login_check")
def check(data: LoginRequest, authorized: None = Depends(verify_key)):
    if check_login(data.gmail, data.passwd) =="pass":
        return {"message": "pass"}
    return {"message": "not found"}


