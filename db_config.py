import os
import psycopg2

def get_db_connection():
    if os.getenv("RENDER_DEPLOYMENT") == "true":
        conn_str = "postgresql://postgres.oooaedmiekwdhjuieoqo:Pcortes170694!@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
        return psycopg2.connect(conn_str)
    else:
        return psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Rebecca17!",
            host="localhost",
            port="5432",
        )