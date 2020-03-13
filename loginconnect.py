import mysql.connector
import os

def create():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="AmazingTheory62",
        database="cloud_formation"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM login_table")
    myresult = (mycursor.fetchone())
    id = myresult[0]
    key = myresult[1]
    region = myresult[2]

    file=open('~/.aws/credentials', 'w')
    file.write(id+','+key)
    file.open('~/.aws/config', 'w')
    file.write(region)