import mysql.connector
print("MySQL Connector installed")
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="joshi@1234",
    database="PharmaOptima"
)
print("Connected to MySQL successfully")
cursor = conn.cursor(buffered=True)