from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Establish the database connection
conn = psycopg2.connect(
    dbname="semifinal",
    user="semifinal_user",
    password="ykBY3gMnOMTVkE67i3c2Mqpb9hE6WFUQ",
    host="dpg-d0amb0pr0fns73cma300-a",
    port="5432",
    sslmode="require"
)

# **1. Financial Data Retrieval & Update**
@app.route('/records/by-year', methods=['GET', 'POST'])
def financial_records():
    if request.method == 'GET':
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

    elif request.method == 'POST':
        # Update the financial data
        data = request.get_json()
        year = data.get('Year')
        revenue = data.get('Revenue')
        cost_of_goods_sold = data.get('CostOfGoodsSold')
        gross_profit = data.get('GrossProfit')
        total_expenses = data.get('TotalExpenses')
        earnings_before_tax = data.get('EarningsBeforeTax')
        taxes = data.get('Taxes')
        net_profit = data.get('NetProfit')
        cash = data.get('Cash')
        debt = data.get('Debt')
        equity_capital = data.get('EquityCapital')
        retained_earnings = data.get('RetainedEarnings')
        total_shareholders_equity = data.get('TotalShareholdersEquity')
        net_earnings = data.get('NetEarnings')
        cash_from_operations = data.get('CashFromOperations')
        investment_in_property_and_equipment = data.get('InvestmentInPropertyAndEquipment')
        cash_from_investing = data.get('CashFromInvesting')
        net_cash_change = data.get('NetCashChange')
        opening_cash_balance = data.get('OpeningCashBalance')
        closing_cash_balance = data.get('ClosingCashBalance')

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE financial_records SET
                    revenue = %s, cost_of_goods_sold = %s, gross_profit = %s, total_expenses = %s, 
                    earnings_before_tax = %s, taxes = %s, net_profit = %s,
                    cash = %s, debt = %s, equity_capital = %s, retained_earnings = %s,
                    total_shareholders_equity = %s, net_earnings = %s, cash_from_operations = %s,
                    investment_in_property_and_equipment = %s, cash_from_investing = %s, 
                    net_cash_change = %s, opening_cash_balance = %s, closing_cash_balance = %s
                WHERE "Year" = %s
            """, (revenue, cost_of_goods_sold, gross_profit, total_expenses, earnings_before_tax,
                  taxes, net_profit, cash, debt, equity_capital, retained_earnings, 
                  total_shareholders_equity, net_earnings, cash_from_operations, 
                  investment_in_property_and_equipment, cash_from_investing, net_cash_change,
                  opening_cash_balance, closing_cash_balance, year))
            conn.commit()
            cur.close()
            return jsonify({"message": "Financial record updated successfully"}), 200
        except Exception as e:
            conn.rollback()
            print("Error updating financial record:", e)
            return jsonify({"error": str(e)}), 500


# **2. Retrieve and Update Products Data (Real-time Updates on Purchase)**
@app.route('/purchase', methods=['POST'])
def purchase_product():
    data = request.get_json()
    product_id = data.get('productid')
    quantity_purchased = data.get('quantity')

    try:
        cur = conn.cursor()
        cur.execute("SELECT quantity FROM product WHERE productid = %s;", (product_id,))
        row = cur.fetchone()

        if row is None:
            return jsonify({"error": "Product not found"}), 404

        current_quantity = row[0]

        if current_quantity < quantity_purchased:
            return jsonify({"error": "Insufficient quantity in stock"}), 400

        # Update product quantity
        cur.execute(
            "UPDATE product SET quantity = quantity - %s WHERE productid = %s;",
            (quantity_purchased, product_id)
        )
        conn.commit()
        cur.close()
        return jsonify({"message": "Purchase successful and quantity updated"}), 200
    except Exception as e:
        conn.rollback()
        print("Error in /purchase:", e)
        return jsonify({"error": str(e)}), 500


# **3. Retrieve Inventory Data**
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


# **4. Sales Data Retrieval & Insertion from Receipt Page**
@app.route('/sales', methods=['POST'])
def insert_sale():
    data = request.get_json()
    customer_id = data.get('customerid')
    employee_id = data.get('employeeid')
    product_id = data.get('productid')
    sales_date = data.get('sales_date')

    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO sales (customerid, employeeid, productid, sales_date)
                       VALUES (%s, %s, %s, %s);""", 
                       (customer_id, employee_id, product_id, sales_date))
        conn.commit()
        cur.close()
        return jsonify({"message": "Sale recorded successfully"}), 201
    except Exception as e:
        conn.rollback()
        print("Error inserting sale:", e)
        return jsonify({"error": str(e)}), 500

# **Retrieve Product Data**
@app.route('/products', methods=['GET'])
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
@app.route('/sales', methods=['GET'])
def get_sales():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                s.sale_id, 
                c.name AS customername, 
                e.name AS employeename, 
                p.name AS productname, 
                s.sale_time
            FROM sales s
            JOIN customer c ON s.customerid = c.customerid
            JOIN employee e ON s.employeeid = e.employeeid
            JOIN product p ON s.productid = p.productid
            ORDER BY s.sale_time DESC;
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
                "sales_date": row[4].strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(sales_list)
    except Exception as e:
        print("Error retrieving sales data:", e)
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
