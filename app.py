from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="Motz Auto & Tyres",
    user="postgres",
    password="qwerty"
)

@app.route('/api/data')
def get_data():
    cur = conn.cursor()
    cur.execute("SELECT * FROM product;")
    rows = cur.fetchall()
    cur.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
