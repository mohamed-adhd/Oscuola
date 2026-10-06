from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import os
import bcrypt
import base64
from groq import Groq


GRADE_TABLES = ["first_year_grades", "second_year_grades", "third_year_grades"]
GRADE_KEYS = ["math", "french", "english", "cs", "ph", "scvt"]



def test():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    with open("gp.jpg", "rb") as f:
        img_data = f.read()
    cur.execute("UPDATE users SET pfp = %s ;",(psycopg2.Binary(img_data),) )
    s.commit()
    cur.close()
    s.close()



def report_ts(x,id,tid):
    syear=int(x[0])
    if  syear==7 :
        tn="first_year_grades"
    elif  syear==8 :
        tn="second_year_grades"
    elif  syear==9 :
        tn="third_year_grades"




    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()

    cur.execute(sql.SQL("SELECT * FROM {} WHERE student_id = %s;").format(sql.Identifier(tn)),(id,))
    res = cur.fetchone()
    headers = [col[0] for col in cur.description]
    table = [headers, res]

    cur.execute("SELECT name,aftername FROM students WHERE id = %s;",(id,))
    res=cur.fetchone()
    tempnm = res[0] +" "+ res[1]



    cur.execute("SELECT * FROM students WHERE id = %s;",(id,))
    ress = cur.fetchone()

    headerss = [col[0] for col in cur.description]
    tables = [headerss, ress]
    ak = os.environ["GROK_KEY"]
    client = Groq()
    #models = [m.id for m in client.models.list().data]
    #chat_models = [m for m in models if not any(x in m for x in ("whisper", "tts", "guard"))]
    #print(chat_models)
    #model = chat_models[0]
    response = client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role": "user", "content": "given that these are infos about a student generate a 600 words maximum report abt him , use formal style and professsional tone as your response will be later trnsformed into a pdf . student info :  "+str(tables)+"  . student grades : "+str(table)}],)
    cur.execute("INSERT INTO reports (teacher_id,student,classs,content) VALUES (%s,%s,%s,%s);",(tid,tempnm,x,response.choices[0].message.content))
    s.commit()
    print("api returned "+response.choices[0].message.content)
    cur.close()
    s.close()




    return {"message":True}


def load_reps(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])

    cur = s.cursor()
    cur.execute("SELECT classs,student,content FROM reports WHERE teacher_id = %s;",(id,) )
    res=cur.fetchall()
    cur.close()
    s.close()
    return {"message":res}


def check_login(gmail, pswd):
    try:
        load_dotenv()
        return_value = "STEP 1 OK: .env loaded"

        database_url = os.environ.get("DATABASE_URL")

        if not database_url:
            return "STEP 2 ERROR: DATABASE_URL is missing"

        try:
            s = psycopg2.connect(database_url)
        except Exception as e:
            return f"STEP 3 ERROR: Database connection failed: {e}"

        try:
            cur = s.cursor()
        except Exception as e:
            s.close()
            return f"STEP 4 ERROR: Could not create cursor: {e}"

        try:
            cur.execute("SELECT password FROM users WHERE gmail=%s;",(gmail,))
        except Exception as e:
            cur.close()
            s.close()
            return f"STEP 5 ERROR: SQL query failed: {e}"

        try:
            res = cur.fetchone()
        except Exception as e:
            cur.close()
            s.close()
            return f"STEP 6 ERROR: fetchone() failed: {e}"

        if not res:
            return f"STEP 7 ERROR: User not found for gmail={gmail}"

        stored_password = res[0]

        if not stored_password:
            return "STEP 8 ERROR: User exists, but password field is empty"

        if not isinstance(stored_password, str):
            return f"STEP 8 ERROR: Password is not VARCHAR/string. Type={type(stored_password)}"

        if not stored_password.startswith("$2"):
            return "STEP 9 ERROR: Stored password does not look like a bcrypt hash"
        try:
            password_match = bcrypt.checkpw(
                pswd.encode(),
                stored_password.encode()
            )
        except Exception as e:
            return f"STEP 10 ERROR: bcrypt.checkpw failed: {e}"

        if password_match:
            try:
                cur.execute("SELECT role,name,aftername,pfp,id FROM users WHERE gmail=%s;", (gmail,))
                res = cur.fetchone()
                ps = res[3]
                p64="nopdp"
                if not ps is None:
                    if isinstance(ps, memoryview):
                        ps = ps.tobytes()
                    p64 = base64.b64encode(ps).decode("ascii")
                if res[0]=="student":
                    cur.execute("SELECT id,syear,classs FROM students WHERE gmail=%s;", (gmail,))
                    rs2=cur.fetchone()
                    return {"success": True, "role": res[0], "name": res[1], "aftername": res[2],"pfp":p64,"ids":rs2[0],"class":rs2[1],"year":rs2[2]}
                else:
                    return {"success": True, "role": res[0], "name": res[1], "aftername": res[2],"pfp":p64,"ids":res[4]}

            except Exception as e:
                cur.close()
                s.close()
                return f"STEP 5 ERROR: 2nd SQL query failed: {e}"



        return "STEP 11 ERROR: User found, but password does not match"

    except Exception as e:
        return f"UNEXPECTED ERROR: {type(e).__name__}: {e}"



def gtable(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    for i in range(len(GRADE_TABLES)):
        cur.execute(f"SELECT student_id FROM {GRADE_TABLES[i]} WHERE student_id = %s ;", (id,))
        if cur.fetchone():
            cur.close()
            s.close()
            return GRADE_TABLES[i], i + 1
    cur.close()
    s.close()
    return GRADE_TABLES[0], 1


def gcols(cur, t):
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position ;", (t,))
    cols = [r[0] for r in cur.fetchall()]
    if "student_id" not in cols:
        return []
    return cols[cols.index("student_id") + 1:]


def get_grades(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    t, year = gtable(id)
    cur.execute(f"SELECT * FROM {t} WHERE student_id = %s ;", (id,))
    res = cur.fetchone()
    cols = [d[0] for d in cur.description]
    sub = gcols(cur, t)
    cur.close()
    s.close()
    d = dict(zip(cols, res)) if res is not None else {}
    subs = sub[:-1] if sub else []
    out = {"success": True, "year": year}
    for i in range(len(GRADE_KEYS)):
        out[GRADE_KEYS[i]] = float(d.get(subs[i]) or 0) if i < len(subs) else 0.0
    out["overallg"] = float(d.get(sub[-1]) or 0) if sub else 0.0
    return out



def get_repcontent(name,classs):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT content FROM reports WHERE student = %s AND classs= %s ;", (name,classs))
    cur.fetchone()
    return {"content":res[0]}











def get_class_grades(classs):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT id,name , aftername  FROM students WHERE classs = %s AND syear=%s;", (int(classs[0]), int(classs[2])))
    res = cur.fetchall()
    ids = [st[0] for st in res]
    t = GRADE_TABLES[0]
    year = 1
    for i in range(len(GRADE_TABLES)):
        if len(ids) == 0:
            break
        cur.execute(f"SELECT student_id FROM {GRADE_TABLES[i]} WHERE student_id = ANY(%s) ;", (ids,))
        if cur.fetchone():
            t = GRADE_TABLES[i]
            year = i + 1
            break
    sub = gcols(cur, t)
    subs = sub[:-1] if sub else []
    got = {}
    if len(ids) > 0 and len(sub) > 0:
        cur.execute(f"SELECT * FROM {t} WHERE student_id = ANY(%s) ;", (ids,))
        cols = [d[0] for d in cur.description]
        for r in cur.fetchall():
            d = dict(zip(cols, r))
            g = {"success": True, "year": year}
            for i in range(len(GRADE_KEYS)):
                g[GRADE_KEYS[i]] = float(d.get(subs[i]) or 0) if i < len(subs) else 0.0
            g["overallg"] = float(d.get(sub[-1]) or 0)
            got[d["student_id"]] = g
    cur.close()
    s.close()
    rows = []
    for st in res:
        g = got.get(st[0])
        if g is None:
            g = {"success": True, "year": year}
            for k in GRADE_KEYS:
                g[k] = 0.0
            g["overallg"] = 0.0
        rows.append({"id": st[0], "name": st[1], "aftername": st[2], "grades": g})
    return {"success": True, "data": rows}

def getstudents(classs,year):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT id,name , aftername  FROM students WHERE classs = %s AND syear=%s;", (classs,year))
    res = cur.fetchall()
    cur.close()
    s.close()
    return res




def get_classes(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT yeary,classs FROM classes WHERE teacher_id = %s ;", (id,))
    res = cur.fetchall()

    cur.close()
    s.close()

    classes = [f"{yeary}A{classs}" for yeary, classs in res]
    ss = {
        "success": True,
        "data": classes
    }
    return ss









def get_reqs(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT DISTINCT r.name, r.aftername, r.classs FROM requests r JOIN classes c ON LEFT(r.classs, 1) = c.yeary WHERE c.teacher_id = %s;", (id,))
    res = cur.fetchall()
    cur.close()
    s.close()
    ss = {
        "success": True,
        "data": res
    }
    return ss

















def timetable(classs, year):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT tb FROM timetables WHERE year = %s AND class=%s;", (year,classs))
    res = cur.fetchone()
    if res is None:
        cur.close()
        s.close()
        return {"success":False,"tb":""}
    if isinstance(res[0], memoryview):
        ps = res[0].tobytes()
    else:
        ps = res[0]
    p64 = base64.b64encode(ps).decode("ascii")
    cur.close()
    s.close()
    return {"success":True,"tb":p64}






def get_alerts_1st(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT message FROM alerts_1st WHERE student_id = %s ;", (id,))
    res = cur.fetchall()
    cur.close()
    s.close()
    ss = {
        "success": True,
        "data": res
    }

    return  ss





