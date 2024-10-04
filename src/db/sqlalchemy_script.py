from typing import Any, Dict, List, Optional

from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class SQLAlchemyDatabase:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def connect(self):
        try:
            self.engine.connect()
            print("Connected to the database")
        except SQLAlchemyError as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        self.engine.dispose()
        print("Database connection closed")

    def execute_script(self, script_file: str):
        try:
            with open(script_file, 'r') as file:
                sql_script = file.read()
            with self.engine.begin() as conn:
                conn.execute(text(sql_script))
            print(f"Script {script_file} executed successfully")
        except SQLAlchemyError as e:
            print(f"Error executing script: {e}")

    def execute_query(self, query: str, params: Dict[str, Any] = None):
        try:
            with self.engine.begin() as conn:
                if params:
                    conn.execute(text(query), params)
                else:
                    conn.execute(text(query))
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            with self.engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                return [dict(row) for row in result]
        except SQLAlchemyError as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        try:
            with self.engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                row = result.fetchone()
                return dict(row) if row else None
        except SQLAlchemyError as e:
            print(f"Error fetching data: {e}")
            return None

    def insert(self, table: str, data: Dict[str, Any]):
        table_obj = Table(table, self.metadata, autoload_with=self.engine)
        try:
            with self.engine.begin() as conn:
                conn.execute(table_obj.insert().values(**data))
        except SQLAlchemyError as e:
            print(f"Error inserting data: {e}")

    def update(self, table: str, data: Dict[str, Any], condition: str):
        table_obj = Table(table, self.metadata, autoload_with=self.engine)
        try:
            with self.engine.begin() as conn:
                conn.execute(table_obj.update().where(text(condition)).values(**data))
        except SQLAlchemyError as e:
            print(f"Error updating data: {e}")

    def delete(self, table: str, condition: str):
        table_obj = Table(table, self.metadata, autoload_with=self.engine)
        try:
            with self.engine.begin() as conn:
                conn.execute(table_obj.delete().where(text(condition)))
        except SQLAlchemyError as e:
            print(f"Error deleting data: {e}")

    def table_exists(self, table_name: str) -> bool:
        return self.engine.dialect.has_table(self.engine, table_name)


    # SQLite connection string
    