from flask import Blueprint, jsonify, request
from db import get_db_connection, release_db_connection

# Create the blueprint
stock_bp = Blueprint('stock', __name__)


# Define the search endpoint
@stock_bp.route('/search_stocks', methods=['GET'])
def search_stocks():
    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:

        conn = get_db_connection()
        cur = conn.cursor()

        # Using ILIKE for case-insensitive partial matching
        query = """
            SELECT symbol, company_name 
            FROM company_overview 
            WHERE symbol ILIKE %s OR company_name ILIKE %s
            LIMIT 10
        """
        like_query = f"%{search_query}%"
        cur.execute(query, (like_query, like_query))
        rows = cur.fetchall()

        # Format results as a list of dictionaries
        results = [{'symbol': row[0], 'company_name': row[1]} for row in rows]
    except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            release_db_connection(conn)  # Use release_db_connection instead of conn.close()

    
    return jsonify(results)
