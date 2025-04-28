import psycopg2

# Database connection
conn = psycopg2.connect(
    host="dpg-d0657qbuibrs73e83q0g-a",  # e.g., localhost or the host of your database
    dbname="postgres_7oco",  # your database name
    user="postgres_7oco_user",  # your database username
    password="QzYY3Fws5ws2Id66PTESQvNiH7Vonc2z",  # your database password
)

# Create a cursor object
cur = conn.cursor()

# Function to check 'Year' data across all tables
def check_years('/year'):
    tables = [
        'financial_records',
        'incomeStatement',
        'balanceSheet',
        'cashFlowStatement'
    ]
    
    for table in tables:
        try:
            # Query to check the 'Year' data in each table
            cur.execute(f'SELECT DISTINCT "Year" FROM {table};')
            rows = cur.fetchall()
            
            # Print out the available years in each table
            print(f"Years in {table}:")
            if rows:
                for row in rows:
                    print(row[0])
            else:
                print(f"No years found in {table}.")
            print("-" * 50)

        except Exception as e:
            print(f"Error with table {table}: {e}")

# Run the function to check years in all tables
check_years()

# Close the cursor and connection
cur.close()
conn.close()
