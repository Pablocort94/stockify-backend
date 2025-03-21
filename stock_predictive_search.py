from flask import Blueprint, jsonify, request
import psycopg2

# Create the blueprint
stock_bp = Blueprint('stock', __name__)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432"
    )

# Define the search endpoint
@stock_bp.route('/search_stocks', methods=['GET'])
def search_stocks():
    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'error': 'Query parameter is required'}), 400

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
    cur.close()
    conn.close()

    # Format results as a list of dictionaries
    results = [{'symbol': row[0], 'company_name': row[1]} for row in rows]
    return jsonify(results)