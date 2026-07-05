from database import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT NOW();")
    print("✅ Database Connected Successfully!")
    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection Failed")
    print(e)