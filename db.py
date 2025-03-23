import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()


# Create a connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

def get_db_connection():
    """Get a connection from the pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Return a connection to the pool."""
    db_pool.putconn(conn)