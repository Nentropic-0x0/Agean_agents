import sqlite3
from typing import Any, List, Optional, Tuple


class SQLite3Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def execute_script(self, script_file: str):
        try:
            with open(script_file, 'r') as file:
                sql_script = file.read()
            self.cursor.executescript(sql_script)
            self.conn.commit()
            print(f"Script {script_file} executed successfully")
        except sqlite3.Error as e:
            print(f"Error executing script: {e}")

    def execute_query(self, query: str, params: Tuple = None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query: str, params: Tuple = None) -> List[Tuple]:
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Tuple]:
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def insert(self, table: str, data: dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def update(self, table: str, data: dict, condition: str):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute_query(query, tuple(data.values()))

    def delete(self, table: str, condition: str):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    def table_exists(self, table_name: str) -> bool:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(query, (table_name,))
        return bool(result)

# Example usage
if __name__ == "__main__":
    db = SQLite3Database("example.db")
    db.connect()

    # Execute a SQL script
    db.execute_script("create_tables.sql")

    # Insert data
    db.insert("users", {"name": "John Doe", "age": 30})

    # Fetch data
    users = db.fetch_all("SELECT * FROM users")
    print("All users:", users)

    # Update data
    db.update("users", {"age": 31}, "name = 'John Doe'")

    # Delete data
    db.delete("users", "name = 'John Doe'")

    db.close()