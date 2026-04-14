CREATE database PharmaOptima; 
USE PharmaOptima;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  password VARCHAR(100)
);
SHOW TABLES;
SELECT * from users;
CREATE table medicines(
drug_id	varchar(100)	PRIMARY KEY,
drug_name	varchar(100),	
therapeutic_area	varchar(100),	
molecule_type	varchar(100),	
launch_year	int,	
region	varchar(100),	
month_year	varchar(100),	
units_sold	int,	
drug_price	int);
ALTER TABLE medicines ADD expiry_date DATE;
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/pharma_dataset.csv'
INTO TABLE medicines
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(drug_id, drug_name, therapeutic_area, molecule_type, launch_year, region, month_year, units_sold, drug_price);

SELECT * FROM medicines;
UPDATE medicines
SET expiry_date = DATE_ADD(STR_TO_DATE(month_year, '%Y-%m'), INTERVAL 2 YEAR)
WHERE drug_id IS NOT NULL;
