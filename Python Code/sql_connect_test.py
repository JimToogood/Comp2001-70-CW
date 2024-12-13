import pyodbc

server = "dist-6-505.uopnet.plymouth.ac.uk"
database = "COMP2001_JToogood"
username = "JToogood"
password = "JxxU593*"
driver = "{ODBC Driver 17 for SQL Server}"

conn_str = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=Yes;"
    "TrustServerCertificate=Yes;"
    "Connection Timeout=30;"
    "Trusted_Connection=No"
)

try:
    # Open connection to database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Verify current database
    cursor.execute("SELECT DB_NAME()")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")

    # Verify current user
    cursor.execute("SELECT USER_NAME()")
    current_user = cursor.fetchone()
    print(f"Connected as user: {current_user[0]}\n")

    # Create a table
    cursor.execute("""
        CREATE TABLE Users (
            id INT PRIMARY KEY,
            name NVARCHAR(50),
            age INT
        )
    """)
    print("Created table.\n")
    
    # Insert data into table
    cursor.execute("INSERT INTO Users (id, name, age) VALUES (?, ?, ?)", (1, "Jim", 20))
    cursor.execute("INSERT INTO Users (id, name, age) VALUES (?, ?, ?)", (2, "Alice", 21))
    print("Inserted data into table.\n")
    
    # Commit to database
    conn.commit()

    # Select and print from "Users"
    cursor.execute("SELECT * FROM Users")

    for row in cursor.fetchall():
        print(row)
    
    # Delete table from database
    cursor.execute("DROP TABLE Users")
    conn.commit()
    print("\nDeleted table.\n")

except pyodbc.Error as error:
    print(f"An error occurred: {error}")

finally:
    # Close connection to database
    conn.close()
    print("Database closed.")
