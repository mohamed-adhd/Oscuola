from dotenv import load_dotenv
import psycopg2
import os
import bcrypt
from smtplib import SMTP
def insert_request(email,password,classs,name,aftername):
    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        s = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cur.execute("INSERT INTO requests (email, password,classs,name,aftername) VALUES (%s, %s,%s,%s,%s);",(email,s,classs,name,aftername))
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
    try :
        load_dotenv()
        cons = os.environ["CON_STRING"]
        s = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = s.cursor()
        cur.execute("SELECT email,password FROM requests WHERE name = %s AND aftername=%s AND classs=%s ;",
                    (name, aftername, classs))
        res = cur.fetchone()
        if res is None:
            return {"message": "No matching request found"}
        cur.execute("INSERT INTO users (name,aftername,gmail,role,password) VALUES (%s,%s,%s,%s,%s);",(name, aftername, res[0], "student", res[1]))
        s.commit()
        cur.execute("INSERT INTO students (name,aftername,gmail,syear,classs) VALUES (%s,%s,%s,%s,%s);", (name, aftername, res[0],int(classs[2]),int(classs[0])))
        s.commit()
        cur.execute("DELETE FROM requests WHERE name = %s AND aftername=%s AND classs=%s ;", (name, aftername, classs))
        s.commit()
        cur.close()
        s.close()
        return {"message":True}
    except Exception as e:
        cur.close()
        s.close()
        return {"message":f"Insert failed my friend: {e}"}









def delete_it(classs,name,aftername):
    try :
        load_dotenv()
        cons = os.environ["CON_STRING"]
        s = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = s.cursor()
        cur.execute("DELETE FROM requests WHERE name = %s AND aftername=%s AND classs=%s ;", (name, aftername, classs))
        s.commit()
        cur.close()
        s.close()
        return {"message":True}
    except Exception as e:
        cur.close()
        s.close()
        return {"message":f"Insert failed my friend: {e}"}
def modifygrades1st(data):
        try:
            load_dotenv()
            cons = os.environ["CON_STRING"]
            s = psycopg2.connect(os.environ["DATABASE_URL"])
            cur = s.cursor()
            cur.execute("UPDATE first_year_grades SET mathematics= %s,french=%s, english=%s,computer_science= %s,physics= %s, life_and_earth_sciences = %s WHERE student_id = %s;",(data.mathematics, data.french, data.english, data.cs, data.physics, data.sc, data.id))
            s.commit()
            cur.close()
            s.close()
            return {"message": True}
        except Exception as e:
            cur.close()
            s.close()
            return {"message": f"Insert failed my friend: {e}"}



def sendemail(gmail):
    with smtplib.SMTP(smtp.gmail.com,587) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)  
        server.sendmail(sender_email, receiver_email, message.as_string())
