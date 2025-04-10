from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from decimal import Decimal

app = Flask(__name__)
CORS(app)

# DB connection
conn = psycopg2.connect(
    dbname="whizz75",
    user="whizz75_user",
    password="0z1ICrtCiBCKxJzOL2QKrC7xsBfuik5u",
    host="dpg-cvqi5g6uk2gs73d6ikn0-a",
    port="5432",
    sslmode="require"
)

@app.route('/api/data')
def get_data():
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
                "sellingprice": float(r[3]) if isinstance(r[3], Decimal) else r[3],
                "quantity": r[4]
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
