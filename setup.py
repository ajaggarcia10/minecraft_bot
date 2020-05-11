import sqlite3

conn = sqlite3.connect('minecraft.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS worlds (World_Name TEXT, Location_Name TEXT, 
X INTEGER, Y INTEGER, Z INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS maps (World_Name TEXT, Seed_Number 
INTEGER, Map TEXT)''')

c.execute('''INSERT INTO worlds VALUES ('Solo_Queue', 'Base', 1500, 70, 150)''')


conn.commit()

