import sqlite3


def get_table_info(database_path):
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Query to retrieve the names and schemas of all tables in the database
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if len(tables) == 4:
            print("The database has exactly 4 tables:")
            for table in tables:
                table_name, table_schema = table
                print(f"\nTable Name: {table_name}")
                print(f"Schema:\n{table_schema}")
        else:
            print(f"The database has {len(tables)} tables, which is not equal to 2.")
            for table in tables:
                table_name, table_schema = table
                print(f"\nTable Name: {table_name}")
                print(f"Schema:\n{table_schema}")
                
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()


def get_table_content(database_path, table_name, limit=10):
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Query to fetch all rows from the table (up to the limit)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        rows = cursor.fetchall()
        
        if rows:
            print(f"Content of the table '{table_name}':")
            for row in rows:
                print(row)
        else:
            print(f"The table '{table_name}' is empty.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()




def remove_null_uniqname_researchers(database_path):
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # SQL command to delete rows where 'uniqname' is NULL
        cursor.execute("DELETE FROM Researchers WHERE uniqname IS NULL;")
        conn.commit()  # Commit the changes
        print("Rows with NULL uniqname removed from Researchers.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

def get_researcher_names(database_path):
    '''
    returns 
    '''
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    try:
        # Query to select all entries from the 'NameFull' column in 'Researchers'
        cursor.execute("SELECT NameFull FROM Researchers;")
        names = cursor.fetchall()  # Fetch all results
        #need to ref by for name in names and then name[0]
        if names:
            return names
        else:
            print("No researchers found.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

DATABASE_PATH = '/home/hudah/expert_field_project/data_pipeline/database/experts.db'
# get_researcher_names()
get_table_info('/home/hudah/expert_field_project/data_pipeline/database/experts.db')
# get_table_content('/home/hudah/expert_field_project/data_pipeline/database/experts.db', 'publications')
# remove_null_uniqname_researchers()