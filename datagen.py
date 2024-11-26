import sqlite3

#This section of code is used to generate a database when ran with the components listed


conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE LoginDetails (
          Student text UNIQUE NOT NULL,
          Password text NOT NULL,
          Email text NOT NULL UNIQUE
          )""")

c.execute("""CREATE TABLE TeacherDetails (
          Teacher text UNIQUE NOT NULL,
          Password text NOT NULL,
          Email text NOT NULL UNIQUE
          )""")

c.execute("""CREATE TABLE AdminDetails (
          Admin text UNIQUE NOT NULL,
          Password text NOT NULL,
          Email text NOT NULL UNIQUE
          )""")

c.execute("""CREATE TABLE Bookings (
          Student_Name text NOT NULL,
          Subject text NOT NULL,
          Teacher_Name text NOT NULL,
          Date text NOT NULL,
          Time text NOT NULL
          )""")

conn.commit()

conn.close()