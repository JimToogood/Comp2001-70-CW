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
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT DB_NAME()")
    print(f"\nConnected to database: {cursor.fetchone()[0]}")
    cursor.execute("SELECT USER_NAME()")
    print(f"Connected as user: {cursor.fetchone()[0]}\n")

    columns = [
        "id INT IDENTITY(1,1) PRIMARY KEY",
        "lname VARCHAR(25) UNIQUE",
        "fname VARCHAR(25)",
        "timestamp DATETIME",
    ]

    create_table_cmd = f'CREATE TABLE person ({",".join(columns)})'
    cursor.execute(create_table_cmd)
    cursor.commit()

    people = [
        "'Grace', 'Hopper', '2024-11-19 16:15:10'",
        "'Tim', 'Berners-Lee', '2024-11-19 16:15:13'",
        "'Ada', 'Lovelace', '2024-11-19 16:15:27'",
    ]

    for person_data in people:
        insert_cmd = f"INSERT INTO person VALUES ({person_data})"
        cursor.execute(insert_cmd)

    cursor.commit()

    cursor.execute("SELECT * FROM person")
    people = cursor.fetchall()
    
    for person in people:
        print(person)

except pyodbc.Error as error:
    print(f"An error occurred: {error}")

finally:
    cursor.execute("DROP TABLE person")
    conn.commit()

    conn.close()
    print("\nDatabase closed.\n")
