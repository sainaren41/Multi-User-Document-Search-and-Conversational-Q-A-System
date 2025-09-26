import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Drop old tables if they exist
c.execute("DROP TABLE IF EXISTS users;")
c.execute("DROP TABLE IF EXISTS documents;")

conn.commit()
conn.close()

print("✅ Both tables dropped successfully")
