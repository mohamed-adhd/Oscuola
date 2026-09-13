from dotenv import load_dotenv
import psycopg2
import os
import bcrypt
def insert_request(email,password):
    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        s = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cur.execute("INSERT INTO requests (email, password) VALUES (%s, %s);",(email,s))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return (f"Insert failed my friend: {e}")
def postit(subject,msg):
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute("INSERT INTO students_posts (subj, msg) VALUES (%s, %s);", (subject, msg))
        conn.commit()
        cur.close()
        conn.close()
        return {"message":True}
    except Exception as e:
        conn.close()
        return (f"Insert failed my friend: {e}")




def accept_it(classs,name,aftername):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT email,password FROM requests WHERE name = %s AND aftername=%s AND class=%s ;", (name,aftername,classs))
    res = cur.fetchone()
    cur.execute("INSERT INTO users (name,aftername,gmail,role,password,) VALUES (%s,%s,%s,%s,%s);)",(name,aftername,res[0],"student",res[1]))
    cur.execute("INSERT INTO  (name,aftername,gmail,role,password,) VALUES (%s,%s,%s,%s,%s);)",(name,aftername,res[0],"student",res[1]))




    cur.close()
    s.close()

