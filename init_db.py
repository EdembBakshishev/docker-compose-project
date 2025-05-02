import psycopg2
from psycopg2 import sql

DB_PARAMS = {
    "dbname": "smmhub",
    "user": "user",
    "password": "password",
    "host": "db"
}

conn = psycopg2.connect(**DB_PARAMS)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL
)
""")

conn.commit()
cursor.close()
conn.close()

print("Database initialized!")
