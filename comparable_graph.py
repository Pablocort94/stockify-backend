from flask import Blueprint, jsonify
from db import get_db_connection, release_db_connection

# Create a blueprint for stock screener
graphdata_bp = Blueprint('graph_data', __name__)


@graphdata_bp.route('/graph_data', methods=['GET'])
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
        SELECT *
        FROM graph_information
        """
        cur.execute(query)
      
        rows = cur.fetchall()# agarra todas las filas
        columns = [desc[0] for desc in cur.description]# genera un listado de lso headers de la tabla
        data = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        # Handle any errors that occur
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        
    finally:
        # Ensure the cursor and connection are properly closed
        if 'cur' in locals():
            cur.close()
        release_db_connection(conn)

    return jsonify({'data': data})



