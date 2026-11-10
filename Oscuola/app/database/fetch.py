from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import os
import bcrypt
import base64
from groq import Groq
import hashlib


GRADE_TABLES = ["first_year_grades", "second_year_grades", "third_year_grades"]
GRADE_KEYS = ["math", "french", "english", "cs", "ph", "scvt"]



def test():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    with open("gp.jpg", "rb") as f:
        img_data = f.read()
    cur.execute("UPDATE timetables SET tb = %s ;",(psycopg2.Binary(img_data),) )
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
        load_dotenv()
        database_url = os.environ.get("DATABASE_URL")
        s = psycopg2.connect(database_url)
        cur = s.cursor()
        cur.execute("SELECT password FROM users WHERE gmail=%s;",(gmail,))

        res = cur.fetchone()

        if not res:
            return {"message":False,"detail":"gmail" }
        stored_password = res[0]


        password_match = bcrypt.checkpw(
            pswd.encode(),
            stored_password.encode()
        )

        if password_match:
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
        else :
            return {"message": False, "detail": "pass"}


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
    res=cur.fetchone()
    return {"content":res[0]}

def lspci():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT yeary,classs FROM classes ;")
    res=cur.fetchall()


    lt=[]
    for row in res:
        lt.append(str(row[0])+"A"+str(row[1]))

    cur.close()
    return {"content":lt}






def lstuds():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT name,aftername FROM students ;")
    res=cur.fetchall()


    lt=[]
    for row in res:
        lt.append(str(row[0])+" "+str(row[1]))
    cur.close()
    return {"content":lt}

def fetchadmn():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE role='student';")
    res=cur.fetchone()
    ts=res[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE role='teacher';")
    res = cur.fetchone()
    tt = res[0]
    cur.execute("SELECT COUNT(*) FROM users ;")
    res=cur.fetchone()
    ta=res[0]
    cur.close()
    s.close()
    return {"s":ts,"t":tt,"tot":ta}



def fetchstoclass():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT COUNT(*) FROM students WHERE syear=7;")
    res=cur.fetchone()
    ts=res[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE syear=8;")
    res = cur.fetchone()
    tt = res[0]
    cur.execute("SELECT COUNT(*) FROM students WHERE syear=9;")
    res=cur.fetchone()
    ta=res[0]
    cur.close()
    s.close()
    return {"7":ts,"8":tt,"9":ta}

def recreg():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT name,aftername FROM users ORDER BY created DESC LIMIT 5;")
    res=cur.fetchall()
    s.close()
    return {"data":res}




def lstuds():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT name,aftername FROM students ;")
    res=cur.fetchall()


    lt=[]
    for row in res:
        lt.append(str(row[0])+" "+str(row[1]))
    cur.close()
    return {"content":lt}
def lstch():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT name,aftername,id  FROM teachers ;")
    res=cur.fetchall()
    return {"data":res}







def lsusr():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT name,aftername,gmail,role FROM users ;")
    res=cur.fetchall()
    cur.close()
    return {"data":res}






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

def getstudents(year,classs):
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




def resetpass(passwd,token):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    nnn=hashlib.sha256(token.encode()).hexdigest()
    cur.execute("SELECT gmail,used FROM tokens WHERE hash = %s ;", (nnn,))
    res = cur.fetchone()
    if res is None :
        cur.close()
        s.close()
        return {"message": "invalid key"}
    if res[1] == True :
        cur.close()
        s.close()
        return {"message":"used key"}
    hashed = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt(rounds=12)).decode()
    cur.execute("UPDATE users SET password = %s WHERE gmail= %s;", (hashed,res[0]))
    s.commit()
    cur.execute("UPDATE tokens SET used = TRUE WHERE hash = %s ;", (nnn,))
    s.commit()

    cur.close()
    s.close()
    return {"message":"password updated"}


MAX_GRADE = 20.0


def teacher_dash(tid):
    load_dotenv()
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute("""
        SELECT c.yeary, c.classs, COUNT(st.id), COALESCE(SUM(COALESCE(g.overall_grade, 0)), 0)
        FROM classes c
        LEFT JOIN students st ON st.syear = c.yeary AND st.classs = c.classs
        LEFT JOIN (
            SELECT student_id, overall_grade FROM first_year_grades
            UNION ALL
            SELECT student_id, overall_grade FROM second_year_grades
            UNION ALL
            SELECT student_id, overall_grade FROM third_year_grades
        ) g ON g.student_id = st.id
        WHERE c.teacher_id = %s
        GROUP BY c.yeary, c.classs
        ORDER BY c.yeary, c.classs;
    """, (tid,))
    grade_rows = cur.fetchall()
    cur.execute("""
        SELECT st.syear, st.classs, COUNT(*)
        FROM absence a
        JOIN students st ON st.id = a.id
        JOIN classes c ON c.yeary = st.syear AND c.classs = st.classs
        WHERE c.teacher_id = %s
        GROUP BY st.syear, st.classs;
    """, (tid,))
    absent = {(r[0], r[1]): r[2] for r in cur.fetchall()}
    cur.execute("""
        SELECT COUNT(*)
        FROM requests r
        JOIN classes c ON r.classs = c.yeary::text || 'A' || c.classs::text
        WHERE c.teacher_id = %s;
    """, (tid,))
    pending = cur.fetchone()[0]
    cur.close()
    conn.close()
    classes = []
    total_sum = 0.0
    total_count = 0
    total_abs = 0
    for yeary, classs, count, gsum in grade_rows:
        gsum = float(gsum)
        rate = (gsum / count / MAX_GRADE * 100) if count else 0.0
        ab = absent.get((yeary, classs), 0)
        total_sum += gsum
        total_count += count
        total_abs += ab
        classes.append({"name": f"{yeary}A{classs}", "rate": round(rate, 1), "absences": ab})
    overall = (total_sum / total_count / MAX_GRADE * 100) if total_count else 0.0
    return {"success": True, "rate": round(overall, 1), "absences": total_abs, "requests": pending, "classes": classes}
