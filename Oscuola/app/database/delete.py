import os
import psycopg2
from dotenv import load_dotenv

GRADE_TABLES = ("first_year_grades", "second_year_grades", "third_year_grades")
ALERT_TABLES = ("alerts_1st", "alerts_2nd", "alerts_3rd")


def deluser(gmail, role, name, aftername):
    load_dotenv()
    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        with conn:
            with conn.cursor() as cur:

                if role == "student":
                    cur.execute(
                        "SELECT id FROM students "
                        "WHERE gmail = %s AND name = %s AND aftername = %s;",
                        (gmail, name, aftername),
                    )
                    res = cur.fetchone()
                    if res is None:
                        raise ValueError("Student not found")
                    student_id = res[0]
                    for table in ALERT_TABLES + GRADE_TABLES:
                        cur.execute(
                            f"DELETE FROM {table} WHERE student_id = %s;",
                            (student_id,),
                        )

                    cur.execute("DELETE FROM students WHERE id = %s;", (student_id,))

                elif role == "teacher":
                    cur.execute(
                        "SELECT id FROM teachers "
                        "WHERE gmail = %s AND name = %s AND aftername = %s;",
                        (gmail, name, aftername),
                    )
                    res = cur.fetchone()
                    if res is None:
                        raise ValueError("Teacher not found")
                    teacher_id = res[0]
                    cur.execute(
                        "UPDATE students SET classs = NULL "
                        "WHERE classs IN (SELECT classs FROM classes WHERE teacher_id = %s);",
                        (teacher_id,),
                    )
                    cur.execute("DELETE FROM classes WHERE teacher_id = %s;", (teacher_id,))
                    cur.execute("DELETE FROM reports WHERE teacher_id = %s;", (teacher_id,))
                    cur.execute("DELETE FROM requests WHERE email = %s;", (gmail,))
                    cur.execute("DELETE FROM teachers WHERE id = %s;", (teacher_id,))

                else:
                    raise ValueError(f"Unknown role: {role}")
                cur.execute(
                    "DELETE FROM users WHERE gmail = %s AND role = %s;",
                    (gmail, role),
                )

        return {"message": True}

    except Exception as e:
        return {"message": f"Delete failed: {e}"}
    finally:
        if conn:
            conn.close()