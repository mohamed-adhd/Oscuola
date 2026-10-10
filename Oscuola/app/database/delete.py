from dotenv import load_dotenv
import psycopg2
import os



def deluser(gmail , role,name,aftername):
    try:
            load_dotenv()
            cons = os.environ["CON_STRING"]
            s = psycopg2.connect(os.environ["DATABASE_URL"])
            cur = s.cursor()
            cur.execute("DELETE FROM users WHERE gmail = %s AND role=%s  ;",(gmail,role))
            s.commit()
            if role == "student":
                cur.execute("SELECT id,syear FROM students WHERE gmail = %s AND name=%s AND aftername=%s ;", (gmail, role,name,aftername))
                res=cur.fetchone()
                if res[1]==7 :
                    cur.execute("DELETE FROM first_year_grades WHERE student_id=%s ;", (int(res[0])),)
                    s.commit()
                if res[1]==8 :
                    cur.execute("DELETE FROM second_year_grades WHERE student_id=%s ;", (int(res[0])),)
                    s.commit()
                if res[1]==9 :
                    cur.execute("DELETE FROM third_year_grades WHERE student_id=%s ;", (int(res[0])),)
                    s.commit()
                cur.execute("DELETE FROM students WHERE id;", (res[0],))
                s.commit()
            elif role == "teacher":
                cur.execute("DELETE FROM teachers WHERE gmail = %s AND name=%s AND aftername=%s ;", (gmail, role,name,aftername))
                s.commit()
            cur.close()
            s.close()
            return {"message": True}
        except Exception as e:
            cur.close()
            s.close()
            return {"message": f"Insert failed my friend: {e}"}

















