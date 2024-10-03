import os
from sqlalchemy import SQLAlchemyDatabase

def sqlite3_main():
    sqlite_db = SQLAlchemyDatabase("sqlite:///example.db")
    sqlite_db.connect()

    # PostgreSQL connection string
    # postgres_db = SQLAlchemyDatabase("postgresql://username:password@localhost:5432/dbname")
    # postgres_db.connect()

    # Execute a SQL script
    os.chdir(os.path("/Users/nullzero/Documents/repos/agean_cyber/src/db/schemas"))
    
    sql_files = [file for files in os.getcwd() for file in os.listdir(files) if files.endswith(".sql")]
    for file in sql_files:    
        sqlite_db.execute_script(file)
        print(f"Created {file} table")
    
    return print("Done")

    