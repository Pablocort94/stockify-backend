from flask import Blueprint, request, jsonify
from db_config import get_db_connection  # Import from db_config.py

# Create a blueprint for stock screener

compadvscore_bp = Blueprint("competitive_advantage_score", __name__)

'''
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Pcortes170694!",
        host="db.oooaedmiekwdhjuieoqo.supabase.co",
        port="5432",
        
    )

def get_db_connection():
    conn_str = "postgresql://postgres.oooaedmiekwdhjuieoqo:Pcortes170694!@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
    return psycopg2.connect(conn_str)
'''

@compadvscore_bp.route("/competitive_advantage_score", methods=["GET"])
def get_available_fields():
    """
    Endpoint to fetch column names from the 'stock_screener_search' view.
    """
    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to fetch column names from the view
        query = """
        select * from competitive_advantage_score t1
join company_overview t2 on t1.ticker=t2.symbol
        """
        cur.execute(query)

        # Extract column names into a list
        rows = cur.fetchall()  # agarra todas las filas
        columns = [
            desc[0] for desc in cur.description
        ]  # genera un listado de lso headers de la tabla
        data = [dict(zip(columns, row)) for row in rows]

        # Close the database connection
        cur.close()
        conn.close()

        return jsonify({"data": data})
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500
