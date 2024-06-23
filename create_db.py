import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="nakuldesai2510"
)

csor = mydb.cursor()

# csor.execute("CREATE DATABASE our_users")

csor.execute("SHOW DATABASES")

data = csor.fetchall()
for db in data:
    print(db)
