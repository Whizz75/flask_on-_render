from flask import Flask, jsonify, render_template
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

@app.route('/home')
def logoAccess():
    return render_template('index.html')
    
@app.route('/api/records')
def get_records():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM financialRecords;")
        rows = cur.fetchall()
        cur.close()

        print("Fetched financial records:", rows)

        return jsonify(rows)

    except Exception as e:
        print("Error in /api/records:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/data')
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

if __name__ == '__main__':
    app.run(debug=True)
