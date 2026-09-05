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
