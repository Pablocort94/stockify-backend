from flask import Blueprint, jsonify, request
from db_config import get_db_connection  # Import from db_config.py

# Create the blueprint
graphpredictivesearch_bp = Blueprint("comparable_graph_predictive_search", __name__)

'''
# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432",
    )
'''

# Define the search endpoint
@graphpredictivesearch_bp.route("/comparable_graph_predictive_search", methods=["GET"])
def search_searchtickers():
    try:

        conn = get_db_connection()
        cur = conn.cursor()

        # Using ILIKE for case-insensitive partial matching
        query = """
            SELECT symbol, company_name 
            FROM company_overview 
        """
        cur.execute(query)
        rows = cur.fetchall()
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
