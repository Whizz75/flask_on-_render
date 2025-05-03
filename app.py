from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    dbname="semifinal",
    user="semifinal_user",
    password="ykBY3gMnOMTVkE67i3c2Mqpb9hE6WFUQ",
    host="dpg-d0amb0pr0fns73cma300-a",
    port="5432",
    sslmode="require"
)

@app.route('/records/by-year')
def financial_records():
        try:
            cur = conn.cursor()
            cur.execute("""SELECT 
                                fr."Year", 
                                inc.revenue, inc.cost_of_goods_sold, inc.gross_profit, 
                                inc.total_expenses, inc.earnings_before_tax, inc.taxes, inc.net_profit,
                                bal.cash, bal.debt, bal.equity_capital, 
                                bal.retained_earnings, bal.total_shareholders_equity,
                                cf.net_earnings, cf.cash_from_operations, 
                                cf.investment_in_property_and_equipment, cf.cash_from_investing, 
                                cf.net_cash_change, cf.opening_cash_balance, cf.closing_cash_balance
                            FROM financial_records fr
                            LEFT JOIN incomeStatement inc ON fr."Year" = inc."Year"
                            LEFT JOIN balanceSheet bal ON fr."Year" = bal."Year"
                            LEFT JOIN cashFlowStatement cf ON fr."Year" = cf."Year"
                            ORDER BY fr."Year" ASC;""")
            rows = cur.fetchall()
            cur.close()

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
            print("Error in /records/by-year:", e)
            return jsonify({"error": str(e)}), 500

@app.route('/inventory')
def get_inventory():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory;")
        rows = cur.fetchall()
        cur.close()

        result = []
        for r in rows:
            result.append({
                "inventoryid": r[0],
                "brand": r[1],
                "quantity": r[2]
            })

        return jsonify(result)
    except Exception as e:
        print("Error in /inventory:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/products')
def get_products():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        rows = cur.fetchall()
        cur.close()

        products_list = []
        for row in rows:
            products_list.append({
                "productid": row[0],
                "productname": row[1],
                "brandname": row[2],
                "sellingprice": row[3],
                "quantity": row[4]
            })

        return jsonify(products_list)
    except Exception as e:
        print("Error in /products:", e)
        return jsonify({"error": str(e)}), 500
        
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
            JOIN product p ON s.productid = p.productid
            ORDER BY s.sales_date DESC;
        """)
        rows = cur.fetchall()
        cur.close()

        sales_list = []
        for row in rows:
            sales_list.append({
                "salesid": row[0],
                "customername": row[1],
                "employee": row[2],
                "product": row[3],
                "sales_date": row[4].strftime("%Y-%m-%d")
            })

        return jsonify(sales_list)
    except Exception as e:
        print("Error retrieving sales data:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
