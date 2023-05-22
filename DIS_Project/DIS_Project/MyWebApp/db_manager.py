import psycopg2
import psycopg2.extras

class DatabaseManager: 
    def __init__(self, db_name, user, password, host):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
   
        self.conn = psycopg2.connect(
            database=self.db_name,
            user = self.user,
            password = self.password,
            host = self.host,
            
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)      

  
        
    def setup_database(self):

            self.cur.execute("""CREATE TABLE IF NOT EXISTS 
                            users (id  INTEGER PRIMARY KEY, 
                            email VARCHAR(255), 
                            first_name VARCHAR(255), 
                            password VARCHAR(255))""")
            
            
            self.cur.execute("""CREATE TABLE IF NOT EXISTS
                                stocks1 (id INTEGER PRIMARY KEY,
                                symbol VARCHAR(255),
                                name VARCHAR(255),
                                shares INTEGER,
                                price NUMERIC(10,2),
                                total NUMERIC(10,2))
                                """)
            
    
            self.cur.execute("""CREATE TABLE IF NOT EXISTS 
                                favorites (id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                stock_id INTEGER,
                                CONSTRAINT unique_user_stock UNIQUE (user_id, stock_id),
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (stock_id) REFERENCES stocks1 (stock_id))
                                                        """)
             
            
            self.cur.execute(""" CREATE TABLE IF NOT EXISTS 
                                stock_history (id SERIAL PRIMARY KEY,
                                stock_id INTEGER,
                                name VARCHAR(255),
                                growth NUMERIC(10,2),
                                FOREIGN KEY (stock_id) REFERENCES stocks1 (id))
                            """)
            
            
            self.commit()


    def get_cursor(self):
        return self.cur
    
    def commit(self):
         self.conn.commit()
    def close(self):
        pass
        


    def insert_stock(self, symbol, name, open, current_price, total):
        self.cur.execute("""
            INSERT INTO stocks1 (symbol, name, shares, price, total)
            VALUES (%s, %s, %s, %s, %s)
            
                         """, (symbol, name, open, current_price, total))
        self.conn.commit()  

    def get_stock(self):
        self.cur.execute("SELECT * FROM stocks1")    
        stocks = self.cur.fetchall()
        print (stocks)
        return stocks
    
    def delete_stock(self):
        self.cur.execute("DELETE FROM stocks1")
        self.conn.commit()
    
    def add_favorite(self, user_id, stock_id):
        self.cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM favorites WHERE user_id = %s AND stock_id = %s
            ) THEN
                INSERT INTO favorites (user_id, stock_id) VALUES (%s, %s);
            END IF;
        END $$;
        """, (user_id, stock_id, user_id, stock_id))
        self.conn.commit()
   
    def get_user_favorites(self, user_id):
        self.cur.execute("""
        SELECT s.*
        FROM favorites f
        JOIN stocks1 s ON f.stock_id = s.id
        WHERE f.user_id = %s
    """, (user_id,))
        return self.cur.fetchall()
    
    def get_ticker_symbols(self):
        self.cur.execute("SELECT symbol FROM stocks1")
        symbols = self.cur.fetchall()
        return symbols
        
db_manager = DatabaseManager(
    db_name="UID",
    user = "janjohannsen",
    password = "password",
    host = "localhost",
)

DatabaseManager.setup_database(db_manager)