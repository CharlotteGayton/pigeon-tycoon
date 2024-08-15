import sqlite3
from flask import jsonify
import json
import random

class Database:

    def __init__(self, db_name) -> None:
        self.connection = None
        self.cursor = None
        self.db_name = db_name
        with open('pigeon_names.py', 'r') as file:
            self.pigeon_names = json.load(file)['pigeon_names']

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;')

    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def fetch_query(self, query, params=()):
        """Fetch results from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.connection.commit()
    
    def create_table(self, table_name, columns):
        query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns});'
        self.execute_query(query)

    def get_table_names(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        return self.execute_query(query)
    
    def create_tables(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS enclosures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS pigeons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                speed INTEGER,
                stamina INTEGER
            )
        ''')
        
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS pigeon_enclosures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pigeon_id INTEGER,
                enclosure_id INTEGER,
                FOREIGN KEY (pigeon_id) REFERENCES pigeons(id),
                FOREIGN KEY (enclosure_id) REFERENCES enclosures(id)
            )
        ''')

        self.execute_query('''
            CREATE TABLE IF NOT EXISTS finances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                balance REAL DEFAULT 0,
                income REAL DEFAULT 0
            )
        ''')

        self.execute_query('''
            CREATE TABLE IF NOT EXISTS pigeon_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price INTEGER,
                speed INTEGER,
                stamina INTEGER
            )
        ''')

    def add_enclosure(self, name, description):
        self.execute_query('INSERT INTO enclosures (name, description) VALUES (?, ?)', (name, description))

    def add_pigeon(self, name, speed, stamina):
        try:
            self.execute_query('INSERT INTO pigeons (name, speed, stamina) VALUES (?, ?, ?)', (name, speed, stamina))
        except sqlite3.IntegrityError:
            return False
        return True

    def assign_pigeon_to_enclosure(self, pigeon_id, enclosure_id):
        self.execute_query('INSERT INTO pigeon_enclosures (pigeon_id, enclosure_id) VALUES (?, ?)', (pigeon_id, enclosure_id))

    def get_enclosures(self):
        return self.fetch_query('SELECT * FROM enclosures')
    
    def get_pigeons_in_enclosure(self, enclosure_id):
        return self.fetch_query('''
            SELECT p.*
            FROM pigeons p
            JOIN pigeon_enclosures pe ON p.id = pe.pigeon_id
            WHERE pe.enclosure_id = ?
        ''', (enclosure_id,))
    
    def get_pigeons(self):
        return self.fetch_query('SELECT * FROM pigeons')
    
    def create_pigeon_for_sale(self):
        if not self.pigeon_names:
            raise ValueError("No more unique pigeon names available.")
    
        while True:
            name = random.choice(self.pigeon_names)
            
            # Check if the name already exists in the pigeon_store
            existing_pigeon = self.fetch_query('SELECT * FROM pigeon_store WHERE name = ?', (name,))
            if not existing_pigeon:
                break
            else:
                # If the name exists, remove it from the list and try again
                self.pigeon_names.remove(name)
                if not self.pigeon_names:
                    raise ValueError("No more unique pigeon names available.")

        self.pigeon_names.remove(name)
        speed = random.randint(5, 20)
        stamina = random.randint(1, 10)
        price = random.randint(50, 200)
        
        self.execute_query('INSERT INTO pigeon_store (name, price, speed, stamina) VALUES (?, ?, ?, ?)', 
                        (name, price, speed, stamina))
        
    def get_pigeons_for_sale(self):
        return self.fetch_query('SELECT * FROM pigeon_store')
    
    def set_income(self, income):
        self.execute_query('UPDATE finances SET income = ?', (income,))

    def get_income(self):
        return self.fetch_query('SELECT income FROM finances')

    def update_balance(self):
        income = self.get_income()[0][0]
        self.execute_query('UPDATE finances SET balance = balance + ?', (income,))

    def get_balance(self):
        return self.fetch_query('SELECT balance FROM finances')
    
    def set_balance(self, balance):
        self.execute_query('UPDATE finances SET balance = ?', (balance,))

    def buy_pigeon(self, pigeon_id):
        pigeon = self.fetch_query('SELECT * FROM pigeon_store WHERE id = ?', (pigeon_id,))
        if pigeon:
            price = pigeon[0][2]
            balance = self.get_balance()[0][0]
            if balance >= price:
                self.execute_query('DELETE FROM pigeon_store WHERE id = ?', (pigeon_id,))
                self.execute_query('UPDATE finances SET balance = balance - ?', (price,))
                self.add_pigeon(pigeon[0][1], pigeon[0][3], pigeon[0][4])
                return True
        return False
