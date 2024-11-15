import sqlite3

#This section of code is used to generate a database when ran with the components listed


conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE LoginDetails (
          Username text UNIQUE NOT NULL,
          Password text NOT NULL,
          Email text NOT NULL UNIQUE
          )""")
conn.commit()

conn.close()