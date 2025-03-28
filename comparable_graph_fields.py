from flask import Blueprint, request, jsonify
from db_config import get_db_connection  # Import from db_config.py

# Create a blueprint for stock screener
graphfields_bp = Blueprint("graph_fields", __name__)

'''
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432",
    )
'''

@graphfields_bp.route("/graph_fields", methods=["GET"])
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
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'graph_information'
        """
        cur.execute(query)

        # Extract column names into a list
        fields = [row[0] for row in cur.fetchall()]

        # Close the database connection
        cur.close()
        conn.close()

        # Return the list of fields as JSON
        return jsonify({"fields": fields})
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500
