from flask import Blueprint, jsonify
from db import get_db_connection, release_db_connection

# Create a blueprint for stock screener

compadvscore_bp = Blueprint('competitive_advantage_score', __name__)


@compadvscore_bp.route('/competitive_advantage_score', methods=['GET'])
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

    # Return the data in JSON format
    return jsonify({'data': data})