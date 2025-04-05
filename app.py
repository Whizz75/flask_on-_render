import psycopg2

# Update the connection string with your local database details
conn = psycopg2.connect(
    dbname="Motz Auto & Tyres",        # Replace with your actual database name
    user="postgres",          # Replace with your database user
    password="qwerty",  # Replace with your database password
    host="localhost",             # Database host (localhost for local instance)
    port="5432"                   # Default PostgreSQL port
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
