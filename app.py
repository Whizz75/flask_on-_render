from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # 🔥 this enables CORS for all routes

# your DB connection
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
        conn = psycopg2.connect(
            dbname="whizz75",
            user="whizz75_user",
            password="0z1ICrtCiBCKxJzOL2QKrC7xsBfuik5u",
            host="dpg-cvqi5g6uk2gs73d6ikn0-a",
            port="5432",
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        for r in rows:
            print("ROW:", r)  # ✅ Show us what’s in each row

        result = []
        for r in rows:
            result.append({
                "productid": r[0],
                "productname": r[1],
                "brandname": r[2],
                "sellingprice": float(r[3]),  # Make sure r[3] is a number
                "quantity": int(r[4])         # Make sure r[4] is an int
            })

        return jsonify(result)

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
