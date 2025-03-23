from flask import Blueprint, jsonify
from db import get_db_connection, release_db_connection

# Create a blueprint for stock screener
graphfields_bp = Blueprint('graph_fields', __name__)

@graphfields_bp.route('/graph_fields', methods=['GET'])
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

    except Exception as e:
        # Handle any errors that occur
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        
    finally:
        # Ensure the cursor and connection are properly closed
        if 'cur' in locals():
            cur.close()
        release_db_connection(conn)

    return jsonify({'fields': fields})

