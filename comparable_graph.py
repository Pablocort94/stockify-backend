from flask import Blueprint, request, jsonify
import psycopg2

# Create a blueprint for stock screener
graphdata_bp = Blueprint('graph_data', __name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432"
    )

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

        # Close the database connection
        cur.close()
        conn.close()

        return jsonify({'data': data})       
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({'error': str(e)}), 500
    


