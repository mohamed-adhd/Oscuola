import base64
from dotenv import load_dotenv
import psycopg2
import os
import bcrypt
from smtplib import SMTP





def update_tb(content,classs,yeary):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    res=base64.decode(content)

    cur.execute("UPDATE timetables WHERE class = %s AND year = %s SET tb = %s ;", (classs,yeary,psycopg2.Binary(res),))
    s.commit()
    cur.close()
    s.close()


















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
        sendemail(res[0],name)
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
def modifygrades(data):
        try:
            load_dotenv()
            cons = os.environ["CON_STRING"]
            s = psycopg2.connect(os.environ["DATABASE_URL"])
            cur = s.cursor()
            from database.fetch import gtable, gcols, GRADE_KEYS
            vals = [data.mathematics, data.french, data.english, data.cs, data.physics, data.sc]
            for v in vals:
                if v < 0 or v > 20:
                    cur.close()
                    s.close()
                    return {"message": "grades must stay between 0 and 20"}
            t, year = gtable(data.id)
            cur.execute(f"SELECT * FROM {t} WHERE student_id = %s ;", (data.id,))
            res = cur.fetchone()
            sub = gcols(cur, t)
            if not sub:
                cur.close()
                s.close()
                return {"message": f"{t} has no student_id"}
            names = sub[:-1]
            sets = []
            args = []
            total = 0.0
            for i in range(len(names)):
                v = vals[i] if i < len(vals) else 0.0
                sets.append(names[i] + " = %s")
                args.append(v)
                total = total + v
            ov = round(total / len(names), 2) if names else 0.0
            sets.append(sub[-1] + " = %s")
            args.append(ov)
            if res is None:
                ph = ", ".join(["%s"] * (len(names) + 2))
                cols = ", ".join(["student_id"] + names + [sub[-1]])
                cur.execute(f"INSERT INTO {t} ({cols}) VALUES ({ph}) ;", [data.id] + args)
            else:
                cur.execute(f"UPDATE {t} SET {', '.join(sets)} WHERE student_id = %s ;", args + [data.id])
            s.commit()
            cur.close()
            s.close()
            return {"message": True, "year": year, "overallg": ov}
        except Exception as e:
            cur.close()
            s.close()
            return {"message": f"Insert failed my friend: {e}"}



import smtplib
from email.message import EmailMessage

def sendemail(email, name):
    message = EmailMessage()
    message["From"] = "oscuolaa@gmail.com"
    message["To"] = email
    message["Subject"] = "Your Oscuola Account Has Been Activated"

    body = (
        f"Dear {name},\n\n"
        "We're happy to announce that you've been accepted into the Oscuola platform. "
        "Your account has been activated, and you can now log in using your credentials.\n\n"
        "Sincerely,\n"
        "Oscuola Devs (Mohamed-adhd)"
    )
    message.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        load_dotenv()
        cons = os.environ["GMAIL_KEY"]
        server.login("oscuolaa@gmail.com", appmail)
        server.send_message(message)