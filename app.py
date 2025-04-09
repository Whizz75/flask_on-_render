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
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        rows = cur.fetchall()
        cur.close()

        print("📦 All rows from DB:")
        for r in rows:
            print(r)  # This will show what each tuple contains

        return jsonify({"message": "Check server logs for printed rows"})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
