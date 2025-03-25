from flask import Blueprint, jsonify, request
import psycopg2

# Create the blueprint
simulationgame_bp = Blueprint("simulationgame", __name__)


# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Rebecca17!",
        host="localhost",
        port="5432",
    )


# Define the search endpoint
@simulationgame_bp.route("/simulationgame", methods=["GET"])
def simulationgame():
    """
    Endpoint to fetch column names from the 'stock_screener_search' view.
    """
    try:
        # Extract target_year from query parameters
        target_year = request.args.get("target_year", type=int)
        if not target_year:
            return jsonify({"error": "target_year query parameter is required"}), 400

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to fetch column names from the view
        query = """
        SELECT 
    t1.ticker,
    calculate_mean((SELECT ARRAY_AGG(net_profit_margin::NUMERIC))) AS mean_net_profit_margin,
    calculate_mean((SELECT ARRAY_AGG(gross_profit_margin::NUMERIC))) AS mean_gross_profit_margin,
    calculate_mean((SELECT ARRAY_AGG(sga_gross_profit_margin::NUMERIC))) AS sga_gross_profit_margin,
    calculate_mean((SELECT ARRAY_AGG(rnd_gross_profit_margin::NUMERIC))) AS rnd_gross_profit_margin,
    calculate_mean((SELECT ARRAY_AGG(cash_to_current_liabilities_ratio::NUMERIC))) AS cash_to_current_liabilities_ratio,
    calculate_mean((SELECT ARRAY_AGG(roa::NUMERIC))) AS roa,
    calculate_mean((SELECT ARRAY_AGG(longtermdebt_to_net_earnings::NUMERIC))) AS longtermdebt_to_net_earnings,
    calculate_mean((SELECT ARRAY_AGG(debt_to_shequity::NUMERIC))) AS debt_to_shequity,
    calculate_mean((SELECT ARRAY_AGG(roe::NUMERIC))) AS roe,
    calculate_mean((SELECT ARRAY_AGG(capex_to_net_income::NUMERIC))) AS capex_to_net_income,
    calculate_mean((SELECT ARRAY_AGG(dso::NUMERIC))) AS dso,
    calculate_mean((SELECT ARRAY_AGG(roic::NUMERIC))) AS roic,
    calculate_mean((SELECT ARRAY_AGG(accounts_receivables_turnover_ratio::NUMERIC))) AS accounts_receivables_turnover_ratio,
    calculate_cagr(
        (SELECT total_revenue::NUMERIC FROM income_statement WHERE Ticker = t1.ticker ORDER BY left(fiscal_date_ending,4)::INTEGER ASC LIMIT 1),
        (SELECT total_revenue::NUMERIC FROM income_statement WHERE left(fiscal_date_ending,4)::INTEGER = %s -1 AND ticker = t1.ticker),
        10
    ) AS cagr_revenue,
    t2.company_name,
    calculate_mean((SELECT ARRAY_AGG(price_adjusted::NUMERIC) from stock_prices_adjusted where left(trade_date,4)::INTEGER= %s -1 and ticker=t1.ticker)) AS average_price
FROM
    income_statement t1
JOIN
    keyfinancialindicators t4 ON t1.fiscal_date_ending::character varying = t4.fiscal_date_ending AND t1.ticker = t4.ticker
    join company_overview t2 on t2.symbol=t1.ticker
WHERE left(t4.fiscal_date_ending,4)::INTEGER < %s -1
GROUP BY
    t1.ticker,t2.company_name
        """

        # Execute the query with the dynamic target_year
        cur.execute(query, (target_year, target_year, target_year))

        # Extract column names into a list
        rows = cur.fetchall()  # Fetch all rows
        columns = [desc[0] for desc in cur.description]  # Extract column headers
        data = [dict(zip(columns, row)) for row in rows]

        # Close the database connection
        cur.close()
        conn.close()

        return jsonify({"data": data})
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500
