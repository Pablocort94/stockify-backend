from flask import Flask, jsonify
from flask_cors import CORS
from email_service import email_bp, configure_mail
from stock_predictive_search import stock_bp
from stock_screener_available_fields import screenerfields_bp
from stock_screener_search_service import screenersearch_bp
from comparable_graph import graphdata_bp
from comparable_graph_fields import graphfields_bp
from comparable_graph_predictive_search import graphpredictivesearch_bp
from comp_advante_score import compadvscore_bp
from simulationgame import simulationgame_bp
from simulationgameresults import simulationgameresults_bp
from db import get_db_connection, release_db_connection



app = Flask(__name__)
CORS(app)  
configure_mail(app)

# Register all blueprints
blueprints = [
    email_bp, stock_bp, screenerfields_bp, screenersearch_bp,
    graphdata_bp, graphfields_bp, graphpredictivesearch_bp,
    compadvscore_bp, simulationgame_bp, simulationgameresults_bp
]
for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

@app.route('/api/stocks/<string:stock_name>/<string:table_name>', methods=['GET'])
def get_table_data(stock_name, table_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        query = f"SELECT * FROM {table_name} WHERE ticker = %s"
        cur.execute(query, (stock_name,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
    finally:
        cur.close()
        release_db_connection(conn)  # Return connection to pool
    
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)