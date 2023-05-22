#This file is for the database tables 
from app import db
from ConnectToDatabase import get_session
import psycopg2

def create_tables(): 
    conn = psycopg2.connect(
        database="UID",
        user = "janjohannsen",
        password = "password",
        host = "localhost",
        
    )
    
    cur = conn.cursor() 
    cur.execute(""" ALTER TABLE user ADD COLUMN id SERIAL PRIMARY KEY; """)   
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL
                );
                """)

    cur.execute(""" 
                CREATE TABLE IF NOT EXISTS stocks (
                    id SERIAL PRIMARY KEY,
                    stock_name VARCHAR(100) NOT NULL,
                    stock_price VARCHAR(100) NOT NULL,
                    stock_symbol VARCHAR(100) NOT NULL,
                    )""")
    
    conn.commit()
    cur.close()
    conn.close()
    

    