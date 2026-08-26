import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="tokopedia_db",
    user="postgres",
    password="admin"
)

print("✅ PostgreSQL connection successful!")

conn.close()