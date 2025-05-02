from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, origins=["https://whizz75.github.io"])

try:
    conn = psycopg2.connect(
        dbname="semi_final",
        user="semi_final_user",
        password="YpD5zzFgrYOeiwA6DEeKtCnG0dPPfWHV",
        host="dpg-d091ruadbo4c73eekv0g-a",
        port="5432",
        sslmode="require"
    )
except Exception as e:
    print("Database connection failed:", e)

@app.route('/purchase/purchase', methods=['POST', 'OPTIONS'])
def purchase():
    if request.method == 'OPTIONS':
        # Handle preflight request (needed for CORS)
        return '', 200  # Respond with 200 OK to indicate the server accepts the request

    if request.method == 'POST':
        # Your logic to handle the purchase request
        data = request.get_json()
        customer_name = data.get('customer_name')
        payment_method = data.get('payment_method')
        employee_id = data.get('employee_id')
        items = data.get('items')

        # Your processing logic (e.g., save to database, etc.)
        # For now, we simply return the received data for confirmation.
        response_data = {
            "message": "Purchase processed successfully",
            "customer_name": customer_name,
            "payment_method": payment_method,
            "employee_id": employee_id,
            "items": items
        }

        return jsonify(response_data), 200  # Respond with a success message

@app.route('/sales', methods=['GET'])
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
                "sales_date": row[4].strftime("%Y-%m-%d")
            })

        return jsonify(sales_data)
    except Exception as e:
        print("Error in /sales:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/sales', methods=['POST'])
def insert_sale():
    data = request.get_json()
    customer_id = data.get('customerid')
    employee_id = data.get('employeeid')
    product_id = data.get('productid')
    sales_date = data.get('sales_date')

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sales (customerid, employeeid, productid, sales_date)
            VALUES (%s, %s, %s, %s);
        """, (customer_id, employee_id, product_id, sales_date))
        conn.commit()
        cur.close()
        return jsonify({"message": "Sale recorded successfully"}), 201
    except Exception as e:
        conn.rollback()
        print("Error inserting sale:", e)
        return jsonify({"error": str(e)}), 500

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

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE product
            SET productname = %s, brandname = %s, sellingprice = %s, quantity = %s
            WHERE productid = %s;
        """, (
            data['productname'],
            data['brandname'],
            data['sellingprice'],
            data['quantity'],
            product_id
        ))
        conn.commit()
        cur.close()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        print("Error updating product:", e)
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

        result = []
        for r in rows:
            result.append({
                "productid": r[0],
                "productname": r[1],
                "brandname": r[2],
                "sellingprice": float(r[3]),
                "quantity": r[4]
            })

        return jsonify(result)
    except Exception as e:
        print("Error in /products:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/records/by-year')
def get_records_by_year():
    try:
        cur = conn.cursor()
        cur.execute("""
                SELECT 
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
                ORDER BY fr."Year" ASC;
        """)
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
        conn.rollback()
        print("Error in /records/by-year:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
