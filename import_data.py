import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="joshi@1234",
    database="PharmaOptima"
)

cursor = conn.cursor()

with open(r"C:\Users\Uni\Downloads\pharma_dataset.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        query = """
        INSERT INTO medicines
        (drug_id, drug_name, therapeutic_area, molecule_type, launch_year, region, month_year, units_sold, drug_price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(query, row)

conn.commit()
print("Data inserted successfully")