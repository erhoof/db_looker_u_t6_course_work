from model.singleton import Singleton
import sqlite3

class ManagerCore(metaclass=Singleton):

    def create_session(self, login, password, db_filename):
        try:
            with open(db_filename) as f:
                print(f.readlines())
        except IOError:
            return 1

    def create_db_file(self, db_filename):
        db_connect = sqlite3.connect(db_filename)
        c = db_connect.cursor()

        c.execute('''
            CREATE TABLE manufacturers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                ceo_fullname TEXT NOT NULL,
                accountant_fullname TEXT,
                requisites TEXT NOT NULL
            );

            CREATE TABLE contracts (
                id INTEGER PRIMARY KEY,
                manufacturer_id INTEGER NOT NULL,
                conclusion_date TEXT NOT NULL,
                delivery_date TEXT NOT NULL,
                delivery_conditions TEXT
                addon TEXT
            );

            CREATE TABLE product_orders (
                id INTEGER PRIMARY KEY,
                type INTEGER NOT NULL,
                parent_id INTEGER NOT NULL
                product_id INTEGER NOT NULL,
                count INTEGER,
                remain_count INTEGER,
                warehouse_id INTEGER NOT NULL
            );

            CREATE TABLE payments (
                id INTEGER PRIMARY KEY,
                type INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                price TEXT NOT NULL,
                vat TEXT,
                payment_status INTEGER,
                admission_status INTEGER
            );

            CREATE TABLE warehouses (
                id INTEGER PRIMARY KEY,
                address TEXT
            );

            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                product_order_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL
            );

            CREATE TABLE clients (
                id INTEGER PRIMARY KEY,
                fullname TEXT
            );

        ''')

        
