from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

try:
    conn = psycopg2.connect(
        dbname="postgres_7oco",
        user="postgres_7oco_user",
        password="QzYY3Fws5ws2Id66PTESQvNiH7Vonc2z",
        host="dpg-d0657qbuibrs73e83q0g-a",
        port="5432",
        sslmode="require"
    )
except Exception as e:
    print("Database connection failed:", e)

@app.route('/sales')
def get_sales():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                s.salesid,
                CONCAT(c.customerfirstname, ' ', c.customerlastname) AS customername,
                CONCAT(e.employeefirstname, ' ', e.employeelastname) AS employee,
                CONCAT(p.productname, ', ', p.brandname) AS product,
                s.sales_date
            FROM sales s
            JOIN customer c ON s.customerid = c.customerid
            JOIN employee e ON s.employeeid = e.employeeid
            JOIN product p ON s.productid = p.productid;
        """)
        rows = cur.fetchall()
        cur.close()

        sales_data = []
        for row in rows:
            sales_data.append({
                "salesid": row[0],
                "customername": row[1],
                "employee": row[2],
                "product": row[3],
                "sales_date": row[4].strftime("%Y-%m-%d")  # format date nicely
            })

        return jsonify(sales_data)
    except Exception as e:
        print("Error in /sales:", e)
        return jsonify({"error": str(e)}), 500
        
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
        
@app.route('/records/by-year')
def get_records_by_year():
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                fr."Year", 
                -- Income Statement
                inc.revenue, inc.cost_of_goods_sold, inc.gross_profit, 
                inc.total_expenses, inc.earnings_before_tax, inc.taxes, inc.net_profit,

                -- Balance Sheet
                bal.cash, bal.debt, bal.equity_capital, 
                bal.retained_earnings, bal.total_shareholders_equity,

                -- Cash Flow Statement
                cf.net_earnings, cf.cash_from_operations, 
                cf.investment_in_property_and_equipment, cf.cash_from_investing, 
                cf.net_cash_change, cf.opening_cash_balance, cf.closing_cash_balance

            FROM financial_records fr
            JOIN incomeStatement inc ON fr."Year" = inc."Year"
            JOIN balanceSheet bal ON fr."Year" = bal."Year"
            JOIN cashFlowStatement cf ON fr."Year" = cf."Year"
            ORDER BY fr."Year" ASC;
        """)

        rows = cur.fetchall()
        cur.close()

        # Return a flat list instead of nested
        records_list = []
        for row in rows:
            records_list.append({
                "Year": row[0],
                "Revenue": row[1],
                "CostOfGoodsSold": row[2],
                "GrossProfit": row[3],
                "TotalExpenses": row[4],
                "EarningsBeforeTax": row[5],
                "Taxes": row[6],
                "NetProfit": row[7],
                "Cash": row[8],
                "Debt": row[9],
                "EquityCapital": row[10],
                "RetainedEarnings": row[11],
                "TotalShareholdersEquity": row[12],
                "NetEarnings": row[13],
                "CashFromOperations": row[14],
                "InvestmentInPropertyAndEquipment": row[15],
                "CashFromInvesting": row[16],
                "NetCashChange": row[17],
                "OpeningCashBalance": row[18],
                "ClosingCashBalance": row[19]
            })

        return jsonify(records_list)

    except Exception as e:
        conn.rollback()
        print("Error in /records/by-year:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
