from flask import Blueprint, jsonify
from db import get_db_connection, release_db_connection

# Create the blueprint
graphpredictivesearch_bp = Blueprint('comparable_graph_predictive_search', __name__)

# Define the search endpoint
@graphpredictivesearch_bp.route('/comparable_graph_predictive_search', methods=['GET'])
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
        columns = [desc[0] for desc in cur.description]# genera un listado de lso headers de la tabla
        data = [dict(zip(columns, row)) for row in rows]

            # Close the database connection
    except Exception as e:
        # Handle any errors that occur
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        
    finally:
        # Ensure the cursor and connection are properly closed
        if 'cur' in locals():
            cur.close()
        release_db_connection(conn)

    return jsonify({'data': data})
