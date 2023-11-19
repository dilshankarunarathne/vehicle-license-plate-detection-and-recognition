import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vehicle"
)

cursor = mydb.cursor()


def query_plate(plate_num):
    
