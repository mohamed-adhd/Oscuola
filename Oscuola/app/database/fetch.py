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

def check_login(gmail,pswd):
    load_dotenv()
    cons=os.environ["CON_STRING"]
    s=psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    pswd.encode()
    bcrypt.gensalt()
    hs= bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())
    cur.execute("SELECT * FROM users WHERE gmail=%s AND password=%s ;")(gmail,hs)
    res=(cur.fetchone())
    cur.close()
    s.close()
    if res:
       return "pass"
    else:
        return "no"


