import mysql.connector
import os
from dotenv import load_dotenv
def setupConnection():
    try:
        host = os.getenv("HOST")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        database = os.getenv("DATABASE")
        conn = mysql.connector.connect(host = host, user = user, password = password)
        conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        conn = mysql.connector.connect(host = host, user = user, password = password, database = database)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS user 
                    ( id INT NOT NULL AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    password TEXT, 
                    hash_key TEXT, 
                    is_active BOOLEAN DEFAULT true,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    is_admin BOOLEAN DEFAULT false, 
                    PRIMARY KEY (id));""")#user table
        

        c.execute("""CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT NOT NULL,
                    barcode VARCHAR(20),
                    name TEXT,
                    category VARCHAR(100),
                    price FLOAT,
                    stock INT,
                    low_threshold INT default 0,

                    PRIMARY KEY(id)
        )""")#product table

        

        c.execute("""CREATE TABLE IF NOT EXISTS transaction (
                    id INT AUTO_INCREMENT NOT NULL,
                    cashier_id INT NOT NULL,
                    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
                    PRIMARY KEY(id),
                    FOREIGN KEY(cashier_id) REFERENCES user(id)
        )""")#transaction table

        

        c.execute("""CREATE TABLE IF NOT EXISTS sale (
                    id INT AUTO_INCREMENT NOT NULL,
                    product_id INT NOT NULL,
                    transaction_id INT NOT NULL,
                    price FLOAT,
                    discount FLOAT,
                    quantity INT,
                    returned INT DEFAULT 0,
                    PRIMARY KEY(id),
                    FOREIGN KEY(product_id) REFERENCES product(id),
                    FOREIGN KEY(transaction_id) REFERENCES transaction(id)
        )""")#sale table

        

        c.execute("""CREATE TABLE IF NOT EXISTS hold (
                id INT AUTO_INCREMENT NOT NULL,
                customer VARCHAR(100) DEFAULT 'Anonymous',
                cashier_id INT NOT NULL,
                timestamp TIMESTAMP default CURRENT_TIMESTAMP,
                PRIMARY KEY(id),
                FOREIGN KEY(cashier_id) REFERENCES user(id)
        )""")#hold table

        

        c.execute("""CREATE TABLE IF NOT EXISTS hold_product (
                    id INT AUTO_INCREMENT NOT NULL,
                    hold_id INT NOT NULL,
                    product_id INT NOT NULL,
                    price FLOAT,
                    quantity INT,
                    PRIMARY KEY(id),
                    FOREIGN KEY(product_id) REFERENCES product(id),
                    FOREIGN KEY(hold_id) REFERENCES hold(id)
        )""")#hold product

        

        c.execute("""CREATE TABLE IF NOT EXISTS delivery (
                    id INT AUTO_INCREMENT NOT NULL,
                    order_id VARCHAR(50),
                    delivered_by VARCHAR(100),
                    received_by INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY(id),
                    FOREIGN KEY(received_by) REFERENCES user(id)
        )""")#delivery

        

        c.execute("""CREATE TABLE IF NOT EXISTS delivery_product (
                    id INT AUTO_INCREMENT NOT NULL,
                    delivery_id INT,
                    product_id INT,
                    expected INT,
                    delivered INT,
                    PRIMARY KEY(id),
                    FOREIGN KEY(delivery_id) REFERENCES delivery(id),
                    FOREIGN KEY(product_id) REFERENCES product(id)
        )""")

        return [True, conn]



            



    except mysql.connector.errors.ProgrammingError as e:
        return [False, e]

    except mysql.connector.errors.DatabaseError as e:
        return [False, e]