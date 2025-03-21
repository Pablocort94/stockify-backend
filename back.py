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



import psycopg2


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask-Mail with the app instance
configure_mail(app)
app.register_blueprint(email_bp, url_prefix='/api')
app.register_blueprint(stock_bp, url_prefix='/api')
app.register_blueprint(screenerfields_bp, url_prefix='/api')
app.register_blueprint(screenersearch_bp, url_prefix='/api')
app.register_blueprint(graphdata_bp, url_prefix='/api')
app.register_blueprint(graphfields_bp, url_prefix='/api')
app.register_blueprint(graphpredictivesearch_bp, url_prefix='/api')
app.register_blueprint(compadvscore_bp, url_prefix='/api')
app.register_blueprint(simulationgame_bp, url_prefix='/api')
app.register_blueprint(simulationgameresults_bp, url_prefix='/api')




def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/api/stocks/<string:stock_name>/<string:table_name>', methods=['GET'])
def get_table_data(stock_name, table_name): #cuando llamas a la url se activa esta funcion que ontiene el nombre de la tabla y el nombre de la accion
    conn = get_db_connection() # establece la conexion
    cur = conn.cursor() # inicializa el cursor
    #if table_name == "income_statement":
    #    query = f"SELECT total_revenue, cost_of_goods_and_services_sold, gross_profit, research_and_development, selling_general_and_administrative, operating_income, investment_income_net, net_interest_income, other_non_operating_income,income_before_tax,interest_expense, income_tax_expense,net_income,ebit,ebitda, fiscal_date_ending, ticker, reported_currency FROM {table_name} WHERE ticker = %s"
    #elif table_name == "balance_sheet":
    #    query = f"SELECT * FROM {table_name} WHERE ticker = %s"
    #elif table_name == "cash_flow":
    #    query = f"SELECT * FROM {table_name} WHERE ticker = %s"
    #elif table_name == "keyfinancialindicators":
    #    query = f"SELECT * FROM {table_name} WHERE ticker = %s"
    #else:
    #    return jsonify({'error': 'Invalid table name'}), 400
    query = f"SELECT * FROM {table_name} WHERE ticker = %s" #hace el select para el stock name
    cur.execute(query, (stock_name,)) #ejecuta la query
    rows = cur.fetchall()# agarra todas las filas
    columns = [desc[0] for desc in cur.description]# genera un listado de lso headers de la tabla
     # Format data as list of dictionaries
    data = [dict(zip(columns, row)) for row in rows]
    cur.close()
    conn.close()
    return jsonify({'data': data})# te devuelve una lista ordenadita de diccionarios
    


if __name__ == '__main__':
    app.run(debug=True)