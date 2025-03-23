import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()

# Check if we're running on Render (or production)
is_production = os.getenv("IS_PRODUCTION", "false").lower() == "true"

# Create the connection pool conditionally based on environment
if is_production:
    # Use the connection string (dsn) for Render (Supabase)
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=db_url  # Using connection string for production
    )
else:
    # Use individual parameters for local development
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