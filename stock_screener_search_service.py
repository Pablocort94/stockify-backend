from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
import psycopg2.extras

# Create Blueprint
screenersearch_bp = Blueprint('screenersearch_bp', __name__)

@screenersearch_bp.route('/screener/search', methods=['POST'])
def search_stocks():
    try:
        # Parse the JSON request
        filters = request.json.get('filters', [])
        if not filters:
            return jsonify({"error": "No filters provided"}), 400

        # Construct the WHERE clause for the SQL query
        conditions = []
        query_params = []
        for filter_item in filters:
            field = filter_item.get('field')
            condition = filter_item.get('condition')
            value = filter_item.get('value')

            if not field or not condition or value is None:
                return jsonify({"error": f"Invalid filter: {filter_item}"}), 400

            if condition == 'greater_than':
                conditions.append(f"{field} > %s")
            elif condition == 'less_than':
                conditions.append(f"{field} < %s")
            elif condition == 'equal_to':
                conditions.append(f"{field} = %s")
            elif condition == 'between' and isinstance(value, list) and len(value) == 2:
                conditions.append(f"{field} BETWEEN %s AND %s")
                query_params.extend(value)
                continue
            else:
                return jsonify({"error": f"Invalid condition in filter: {filter_item}"}), 400

            query_params.append(value)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # Construct and execute the SQL query
        query = f"SELECT * FROM stock_screener_search WHERE {where_clause} LIMIT 100"
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, query_params)
        results = cur.fetchall()

        # Transform results into a JSON-friendly format
        rows = [dict(row) for row in results]

    except Exception as e:
        # Handle any errors that occur
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        
    finally:
        # Ensure the cursor and connection are properly closed
        if 'cur' in locals():
            cur.close()
        release_db_connection(conn)

    return jsonify({"data": rows, "count": len(rows)})
        
       