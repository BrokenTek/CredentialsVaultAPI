import sqlite3
import json

def export_credentials(json_path):
    """
    Export the data from a specified table in an SQLite database to a JSON file.

    Parameters:
        db_path (str): The path to the SQLite database file.
        json_path (str): The path to the JSON file where the data will be exported.

    Returns:
        None
    """
    # define the path to the db file (this is the default path created at first run of api.py)
    db_path = "instance/creds.db"
    
    # define the name of the table to retrieve data from
    table_name = "credential"
    
    try:
        # connect to the SQLite2 database passed as db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.OperationalError as e:
        print(f"\nError connecting to database: {e}\nPlease check that the database file exists and that the path is correct.\n\
No data exported.\n")
        return
    
    try:
        # retrieve data from the specified table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Error exporting data: {e}")
    
    # get names of fields/columns
    column_names = [description[0] for description in cursor.description]
    
    # convert data to a JSON-compatible format
    data = [dict(zip(column_names, row)) for row in rows]
    
    # write data to a JSON file
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # end connection
    conn.close()
