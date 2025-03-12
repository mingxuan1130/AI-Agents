import sqlite3
import os
import pandas as pd

def get_data_from_database(db_path, sql_path):
    """
    Execute SQL query on the database and return results as a pandas DataFrame.
    
    Args:
        db_path (str): Path to the SQLite database file
        sql_path (str): Path to the SQL query file
        
    Returns:
        pandas.DataFrame: Query results as a DataFrame
    """
    # Read the SQL script
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Connect to the database and execute queries
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_script)

    # Fetch all results and column names
    results = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    # Create a pandas DataFrame from the results
    df = pd.DataFrame(results, columns=col_names)
    
    cursor.close()
    conn.close()
    
    return df

def save_data_to_csv(df, csv_path):
    """
    Save DataFrame to a CSV file.
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        csv_path (str): Path where CSV file will be saved
        
    Returns:
        str: Path to the saved CSV file
    """
    df.to_csv(csv_path, index=False)
    return csv_path 