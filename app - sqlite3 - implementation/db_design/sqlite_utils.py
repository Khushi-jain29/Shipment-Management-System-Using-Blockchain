import sqlite3

def get_db_cursor_obj(database_name):
    cnxn = sqlite3.connect(database_name)
    return cnxn.cursor(), cnxn

def get_create_table_query(tablename, cols, datatypes):
    paired_cols = [f'"{col}" {datatype}' for col, datatype in zip(cols, datatypes)]
    query = f'CREATE TABLE IF NOT EXISTS "{tablename}" ( ' + ', '.join(paired_cols) + ' );'
    print("\nCreate Table Query:\n", query)
    return query

def create_table(cursor, tablename, cols, datatypes):
    query = get_create_table_query(tablename, cols, datatypes)
    cursor.execute(query)
    return True

def get_tables_in_db(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    return tables

def get_db_table_row_count(cursor, table_name):
    cursor.execute(f'SELECT count(*) FROM "{table_name}"')
    return cursor.fetchone()[0]

def generate_insert_query(target_table_name, processed_cols):
    columns_str = ', '.join([f'"{col}"' for col in processed_cols])
    values_placeholder = ', '.join(['?'] * len(processed_cols))
    query = f'INSERT INTO "{target_table_name}" ({columns_str}) VALUES ({values_placeholder})'
    return query

def get_existing_rows_ids(cursor, tablename, filter_by):
    cursor.execute(f'SELECT {filter_by} FROM "{tablename}"')
    return {str(row[0]) for row in cursor.fetchall()}

def filter_unmigrated_rows(cursor, tablename, formatted_rows, filter_by='SourceFileRowOrder', filter_col_index=-1):
    existing_row_ids = get_existing_rows_ids(cursor, tablename, filter_by)
    unmigrated_rows = [row for row in formatted_rows if str(row[filter_col_index]) not in existing_row_ids]
    return unmigrated_rows

# Example usage
cursor, cnxn = get_db_cursor_obj('shipment_management_system.db')
