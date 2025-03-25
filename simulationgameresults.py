from flask import Blueprint, jsonify, request
import psycopg2

# Create the blueprint
simulationgameresults_bp = Blueprint("simulationgameresults", __name__)


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
@simulationgameresults_bp.route("/simulationgameresults", methods=["GET"])
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
select 	t1.ticker, calculate_mean((SELECT ARRAY_AGG(net_profit_margin::NUMERIC))) as mean_net_profit_margin,
 calculate_mean((SELECT ARRAY_AGG(gross_profit_margin::NUMERIC))) as mean_gross_profit_margin,
  calculate_mean((SELECT ARRAY_AGG(sga_gross_profit_margin::NUMERIC))) as sga_gross_profit_margin,
    calculate_mean((SELECT ARRAY_AGG(rnd_gross_profit_margin::NUMERIC))) as rnd_gross_profit_margin,
	    calculate_mean((SELECT ARRAY_AGG(cash_to_current_liabilities_ratio::NUMERIC))) as cash_to_current_liabilities_ratio,
    calculate_mean((SELECT ARRAY_AGG(roa::NUMERIC))) as roa,
    calculate_mean((SELECT ARRAY_AGG(longtermdebt_to_net_earnings::NUMERIC))) as longtermdebt_to_net_earnings,
    calculate_mean((SELECT ARRAY_AGG(debt_to_shequity::NUMERIC))) as debt_to_shequity,
    calculate_mean((SELECT ARRAY_AGG(roe::NUMERIC))) as roe,
    calculate_mean((SELECT ARRAY_AGG(capex_to_net_income::NUMERIC))) as capex_to_net_income,
    calculate_mean((SELECT ARRAY_AGG(dso::NUMERIC))) as dso,
    calculate_mean((SELECT ARRAY_AGG(roic::NUMERIC))) as roic,
    calculate_mean((SELECT ARRAY_AGG(accounts_receivables_turnover_ratio::NUMERIC))) as accounts_receivables_turnover_ratio,
	calculate_cagr(
				(select total_revenue::nUMERIC FROM income_statement WHERE Ticker = t1.ticker and left(fiscal_date_ending,4)::INTEGER = %s),
				(SELECT total_revenue::NUMERIC FROM income_statement WHERE left(fiscal_date_ending,4)::INTEGER = (
             SELECT MAX(LEFT(fiscal_date_ending, 4)::INTEGER)
             FROM income_statement
             WHERE ticker = t1.ticker
         )  AND ticker = t1.ticker),
				(
             SELECT MAX(LEFT(fiscal_date_ending, 4)::INTEGER)
             FROM income_statement
             WHERE ticker = t1.ticker
         )- %s
			) AS cagr_revenue,
			t2.company_name,
    calculate_mean((SELECT ARRAY_AGG(price_adjusted::NUMERIC) from stock_prices_adjusted where left(trade_date,4)::INTEGER= (
             SELECT MAX(LEFT(trade_date, 4)::INTEGER)
             FROM stock_prices_adjusted
             WHERE ticker = t1.ticker
         ) AND ticker = t1.ticker)
    ) AS average_price

 FROM
					income_statement t1
				JOIN
					keyfinancialindicators t4 on t1.fiscal_date_ending::character varying = t4.fiscal_date_ending AND t1.ticker = t4.ticker
					join company_overview t2 on t2.symbol=t1.ticker
								WHERE left(t4.fiscal_date_ending,4)::INTEGER = (
        SELECT MAX(LEFT(fiscal_date_ending, 4)::INTEGER)
        FROM keyfinancialindicators
        WHERE ticker = t4.ticker)
				GROUP BY
					t1.ticker,t2.company_name
        """

        # Execute the query with the dynamic target_year
        cur.execute(query, (target_year, target_year))

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
