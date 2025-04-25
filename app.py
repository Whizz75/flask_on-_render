from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

try:
    conn = psycopg2.connect(
        dbname="whizz75_nzgk",
        user="whizz75_nzgk_user",
        password="0ycwbcpqtmMOd4Qw3p3px0YANWZy5GM1",
        host="dpg-cvrru42li9vc739n4140-a",
        port="5432",
        sslmode="require"
    )
except Exception as e:
    print("Database connection failed:", e)

@app.route('/products')
def get_data():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        rows = cur.fetchall()
        cur.close()

        print("Fetched products:", rows)

        result = []
        for r in rows:
            try:
                result.append({
                    "productid": r[0],
                    "productname": r[1],
                    "brandname": r[2],
                    "sellingprice": float(r[3]),
                    "quantity": r[4]
                })
            except IndexError as err:
                print("Tuple index error:", err)
                continue

        return jsonify(result)

    except Exception as e:
        print("Error in /api/data:", e)
        return jsonify({"error": str(e)}), 500
        
@app.route('/records', methods=['GET'])
def get_records():
    try:
        year = request.args.get('year', type=int)

        # SQL Query to fetch the data by year
        query = """
            SELECT 
                fr."Year", 
                -- Income Statement Data
                is.revenue, 
                is.cost_of_goods_sold, 
                is.gross_profit, 
                is.total_expenses, 
                is.earnings_before_tax, 
                is.taxes, 
                is.net_profit,

                -- Balance Sheet Data
                bs.cash, 
                bs.debt, 
                bs.equity_capital, 
                bs.retained_earnings, 
                bs.total_shareholders_equity,

                -- Cash Flow Statement Data
                cf.net_earnings, 
                cf.cash_from_operations, 
                cf.investment_in_property_and_equipment, 
                cf.cash_from_investing, 
                cf.net_cash_change, 
                cf.opening_cash_balance, 
                cf.closing_cash_balance

            FROM 
                financial_records fr
            JOIN 
                incomeStatement is ON fr."Year" = is."Year"
            JOIN 
                balancesheet bs ON fr."Year" = bs."Year"
            JOIN 
                cashFlowStatement cf ON fr."Year" = cf."Year"
            WHERE fr."Year" = %s
            ORDER BY fr."Year" ASC;
        """

        # Execute the query, if a year is provided
        cur = conn.cursor()
        if year:
            cur.execute(query, (year,))
        else:
            # If no year is provided, get all records
            cur.execute(query)
        
        rows = cur.fetchall()
        cur.close()

        # Prepare result in a structured format
        result = []
        for r in rows:
            result.append({
                "Year": r[0],
                "IncomeStatement": {
                    "Revenue": r[1],
                    "CostOfGoodsSold": r[2],
                    "GrossProfit": r[3],
                    "TotalExpenses": r[4],
                    "EarningsBeforeTax": r[5],
                    "Taxes": r[6],
                    "NetProfit": r[7]
                },
                "BalanceSheet": {
                    "Cash": r[8],
                    "Debt": r[9],
                    "EquityCapital": r[10],
                    "RetainedEarnings": r[11],
                    "TotalShareholdersEquity": r[12]
                },
                "CashFlowStatement": {
                    "NetEarnings": r[13],
                    "CashFromOperations": r[14],
                    "InvestmentInPropertyAndEquipment": r[15],
                    "CashFromInvesting": r[16],
                    "NetCashChange": r[17],
                    "OpeningCashBalance": r[18],
                    "ClosingCashBalance": r[19]
                }
            })

        return jsonify(result)

    except Exception as e:
        print("Error in /records:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
