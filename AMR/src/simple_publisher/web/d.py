import mysql.connector

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host=" 192.168.137.1",
  user="hi",
#   password="your_password"  # Replace with your MySQL password
)

# Create a new database named "demo" if it doesn't exist
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS demo")
print("Database 'demo' created")

# Connect to the "demo" database
mydb = mysql.connector.connect(
  host=" 192.168.137.1",
  user="hi",
#   password="your_password",  # Replace with your MySQL password
  database="demo"
)

# Create a table
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
print("Table 'customers' created")

# Insert data into the table
insert_data = "INSERT INTO customers (name, email) VALUES (%s, %s)"
values = [("John Doe", "john.doe@example.com"), ("Jane Smith", "jane.smith@example.com")]
mycursor.executemany(insert_data, values)
mydb.commit()
print(mycursor.rowcount, "record(s) inserted")

# Fetch data from the table
mycursor.execute("SELECT * FROM customers")
result = mycursor.fetchall()
for row in result:
    print("ID:", row[0])
    print("Name:", row[1])
    print("Email:", row[2])
    print()

# Close the database connection
mydb.close()
