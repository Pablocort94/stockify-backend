import psycopg2
#from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()

# Check if we're running on Render (or production)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """Get a direct database connection (without pooling)."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode="require"
        )
        return conn
    except Exception as e:
        print("❌ Database connection error:", e)
        return None

def release_db_connection(conn):
    """Close the database connection (no pooling)."""
    if conn:
        conn.close()