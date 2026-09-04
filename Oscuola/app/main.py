from fastapi import FastAPI
import database
from Oscuola.app.database.fetch import test

app = FastAPI()
@app.get("/")
def root():
    s=test()
    return {"message": s}
