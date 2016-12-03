import sqlite3
conn = sqlite3.connect('status.db')
c = conn.cursor()
c.execute("UPDATE status SET status=0 WHERE 1")
conn.commit()
conn.close()

