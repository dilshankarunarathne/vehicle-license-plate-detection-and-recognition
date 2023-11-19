import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vehicle"
)

cursor = mydb.cursor()


def query_plate(plate_num):
    cursor.execute("SELECT * FROM vehicle WHERE plate_num = %s", (plate_num,))
    return cursor.fetchall()


def add_info(plate_num, owner_name, owner_phone, owner_address):
    cursor.execute("INSERT INTO vehicle (plate_num, owner_name, owner_phone, owner_address) VALUES (%s, %s, %s, %s)",
                   (plate_num, owner_name, owner_phone, owner_address))
