from dotenv import load_dotenv
import psycopg2
import os
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




