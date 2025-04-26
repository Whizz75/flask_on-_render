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
def get_sales_data():
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                s.salesid,
                c.customername,
                e.(employeefirstname, employeelastname) as employee,
                p.(productname, brandname) as product,
                s.sales_date,
                s.revenue
            FROM sales s
            JOIN customer c ON s.customerid = c.customerid
            JOIN employee e ON s.employeeid = e.employeeid
            JOIN product p ON s.productid = p.productid
            ORDER BY s.sales_date DESC;
        """)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()

        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))

        return jsonify(data)

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
        cur.execute("SELECT * FROM financialRecords;")
        rows = cur.fetchall()
        cur.close()

        columns = [desc[0] for desc in cur.description]

        # Convert data into a structured dict by year
        records_by_year = {}

        for row in rows:
            record = dict(zip(columns, row))
            year = record.get("Year")

            if year not in records_by_year:
                records_by_year[year] = {
                    "IncomeStatement": {},
                    "BalanceSheet": {},
                    "CashFlowStatement": {}
                }

            # Group fields by statement type
            for key, value in record.items():
                if key in ["Year", "id"]:
                    continue
                if key in ["Revenue", "CostOfGoodsSold", "GrossProfit", "TotalExpenses", "EarningsBeforeTax", "Taxes", "NetProfit"]:
                    records_by_year[year]["IncomeStatement"][key] = value
                elif key in ["Cash", "Debt", "EquityCapital", "RetainedEarnings", "TotalShareholdersEquity"]:
                    records_by_year[year]["BalanceSheet"][key] = value
                elif key in ["NetEarnings", "CashFromOperations", "InvestmentInPropertyAndEquipment", "CashFromInvesting", "NetCashChange", "OpeningCashBalance", "ClosingCashBalance"]:
                    records_by_year[year]["CashFlowStatement"][key] = value

        return jsonify(records_by_year)

    except Exception as e:
        print("Error in /records/by-year:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
