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

        c.execute('PRAGMA foreign_keys=ON;')

        c.execute('''
            CREATE TABLE manufacturers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                ceo_fullname TEXT NOT NULL,
                accountant_fullname TEXT,
                requisites TEXT NOT NULL
            );
        ''')

        c.execute('''
            CREATE TABLE contracts (
                id INTEGER PRIMARY KEY,
                manufacturer_id INTEGER NOT NULL,
                conclusion_date TEXT NOT NULL,
                delivery_date TEXT NOT NULL,
                delivery_conditions TEXT
                addon TEXT,
                FOREIGN KEY(manufacturer_id) REFERENCES manufacturers(id)
            );
        ''')

        c.execute('''
            CREATE TABLE product_orders (
                id INTEGER PRIMARY KEY,
                contract_id INTEGER,
                sale_id INTEGER,
                product_id INTEGER NOT NULL,
                count INTEGER,
                remain_count INTEGER,
                warehouse_id INTEGER NOT NULL,
                CHECK(contract_id IS NOT NULL OR sale_id IS NOT NULL),
                FOREIGN KEY(contract_id) REFERENCES contracts(id),
                FOREIGN KEY(sale_id) REFERENCES sales(id),
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(warehouse_id) REFERENCES warehouses(id)
            );
        ''')

        c.execute('''
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY,
                type INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                price TEXT NOT NULL,
                vat TEXT,
                payment_status INTEGER,
                admission_status INTEGER,
                FOREIGN KEY(order_id) REFERENCES product_orders(id)
            );
        ''')

        c.execute('''
            CREATE TABLE warehouses (
                id INTEGER PRIMARY KEY,
                address TEXT
            );
        ''')

        c.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                product_order_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                FOREIGN KEY(product_order_id) REFERENCES product_orders(id),
                FOREIGN KEY(client_id) REFERENCES clients(id)
            );
        ''')

        c.execute('''
            CREATE TABLE clients (
                id INTEGER PRIMARY KEY,
                fullname TEXT
            );
        ''')

        c.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                manufacturer_id INTEGER,
                name TEXT,
                specs TEXT,
                price TEXT,
                packaging TEXT,
                addon TEXT,
                FOREIGN KEY(manufacturer_id) REFERENCES manufacturers(id)
            );
        ''')

        c.execute('''
            CREATE TABLE users(
                id INTEGER PRIMARY KEY,
                login TEXT,
                password_hash TEXT
            );
        ''')

        db_connect.commit()

        
