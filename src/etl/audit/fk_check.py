import sqlite3

conn = sqlite3.connect("data/nifty100.db")

violations = conn.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print("FK Violations:", len(violations))
print(violations)

conn.close()