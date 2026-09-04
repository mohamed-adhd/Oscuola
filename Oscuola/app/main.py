from fastapi import FastAPI
from database.fetch import test

app = FastAPI()
@app.get("/")
def root():
    s=test()
    return {"message": s}
