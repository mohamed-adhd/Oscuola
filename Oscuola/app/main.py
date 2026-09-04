import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
from database.fetch import test
app = FastAPI()

@app.get("/")
def root():
    s = test()
    return {"message": s}