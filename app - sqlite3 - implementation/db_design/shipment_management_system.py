# -*- coding: utf-8 -*-
"""shipment_management_system.ipynb

"""

import sqlite3


def execute_sql_script(file_path, db_path):
    # Open the file containing SQL commands
    with open(file_path, 'r') as file:
        sql_script = file.read()
    
    # Connect to the SQLite database
    cnxn = sqlite3.connect(db_path)
    cursor = cnxn.cursor()

    # Execute the SQL script
    try:
        cursor.executescript(sql_script)
        cnxn.commit()
    except sqlite3.ProgrammingError as e:
        print(f"An error occurred: {e}")
    finally:
        cnxn.close()
        print(f'{file_path} executed.')

# Example usage
db_path = 'shipment_management_system.db'
schema_file_path = 'schema.sql'  # Replace with your SQL script file path
execute_sql_script(schema_file_path, db_path)


database_records_file_path = 'database_records.sql'
execute_sql_script(database_records_file_path, db_path)



cnxn = sqlite3.connect(db_path)
cursor = cnxn.cursor()
def get_tables_in_db(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    return tables
print(f'List of Tables: {get_tables_in_db(cursor)}')

def get_db_table_row_count(cursor, table_name):
    cursor.execute(f'SELECT count(*) FROM "{table_name}"')
    return cursor.fetchone()[0]

print(f"Number of Records in Users: {get_db_table_row_count(cursor, 'Users')}")

print(f"Number of Records in Products: {get_db_table_row_count(cursor, 'Products')}")

print(f"Number of Records in Shipments: {get_db_table_row_count(cursor, 'Shipments')}")

print(f"Number of Records in ShipmentHistory: {get_db_table_row_count(cursor, 'ShipmentHistory')}")
