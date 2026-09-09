from dotenv import load_dotenv
import psycopg2
import os
import bcrypt
import base64
def test():
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    with open("pg.jpg", "rb") as f:
        img_data = f.read()
    cur.execute("UPDATE users SET pfp = %s ;",(psycopg2.Binary(img_data),) )
    s.commit()
    cur.close()
    s.close()
    return {"success": True}
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
                if isinstance(res[3], memoryview):
                    ps = res[3].tobytes()
                p64 = base64.b64encode(ps).decode("ascii")
                return {"success": True, "role": res[0], "name": res[1], "aftername": res[2],"pfp":p64,"id":res[4]}
            except Exception as e:
                cur.close()
                s.close()
                return f"STEP 5 ERROR: 2nd SQL query failed: {e}"



        return "STEP 11 ERROR: User found, but password does not match"

    except Exception as e:
        return f"UNEXPECTED ERROR: {type(e).__name__}: {e}"



def get_grades_1st(id):
    load_dotenv()
    cons = os.environ["CON_STRING"]
    s = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = s.cursor()
    cur.execute("SELECT * FROM first_year_grades WHERE student_id = %s ;", (id,))
    res = cur.fetchone()
    cur.close()
    s.close()
    return {"success": True, "math": res[2], "french": res[3], "english": res[4],"cs":res[5],"ph": res[6], "scvt": res[7], "overallg": res[8]}




















