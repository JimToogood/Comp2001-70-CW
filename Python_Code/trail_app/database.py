import pyodbc
from config import DB_CONFIG


def get_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG["driver"]};"
        f"SERVER={DB_CONFIG["server"]};"
        f"DATABASE={DB_CONFIG["database"]};"
        f"UID={DB_CONFIG["username"]};"
        f"PWD={DB_CONFIG["password"]};"
        "Encrypt=Yes;"
        "TrustServerCertificate=Yes;"
        "Connection Timeout=30;"
        "Trusted_Connection=No"
    )

    return pyodbc.connect(conn_str)
