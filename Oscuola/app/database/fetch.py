from dotenv import load_dotenv
import psycopg2
import os
import bcrypt
def test():
    load_dotenv()
    cons=os.environ["CON_STRING"]
    s=psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT NOW();")
    res=(cur.fetchone())
    cur.close()
    s.close()
    return res
def check_login(gmail, pswd):
    load_dotenv()
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT password FROM users WHERE gmail=%s;", (gmail,))
    res = cur.fetchone()
    cur.close()
    s.close()
    if res and bcrypt.checkpw(pswd.encode(), res[0].encode()):
        return "pass"
    return "no"


