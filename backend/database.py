import sqlite3
from flask import jsonify

class Database:

    def __init__(self, db_name) -> None:
        self.connection = None
        self.cursor = None
        self.db_name = db_name

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
        """Create tables if they do not exist."""
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
                balance INTEGER
            )
        ''')

        self.execute_query('''
            CREATE TABLE IF NOT EXISTS pigeon_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pigeon_id INTEGER,
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