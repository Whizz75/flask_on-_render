from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Replace these values with your actual Render database credentials
conn = psycopg2.connect(
    dbname="motz_auto_and_tyres",  # Use the correct name as seen on Render
    user="whizz75_user",    # e.g., render_user_xxxxx
    password="0z1ICrtCiBCKxJzOL2QKrC7xsBfuik5u",
    host="dpg-cvqi5g6uk2gs73d6ikn0-a",    # e.g., dpg-xxxxxx.databases.render.com
    port="5432",                   # Usually 5432 for PostgreSQL
    sslmode="require"              # Important for Render PostgreSQL connections
)

@app.route('/api/data')
def get_data():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product;")
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
