#!/usr/bin/env python3
"""
Weekly Business Review (WBR) Automation Script

This script automates the process of generating Weekly Business Review reports by:
1. Querying a SQLite database
2. Creating visualizations
3. Sending email reports with charts and data
"""

import os
import sys

# Try to import config file
try:
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the script directory to the Python path
    sys.path.insert(0, script_dir)
    
    # Now try to import the config
    import config
    has_config = True
    print("Successfully loaded config file")
except ImportError as e:
    print(f"Could not import config file: {e}")
    has_config = False

# Import modules from src package
from src.database import get_data_from_database, save_data_to_csv
from src.visualization import create_chart, get_data_insights
from src.email_sender import get_email_credentials, create_email_message, send_email

def main():
    """
    Main function that orchestrates the WBR automation process.
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory for database and SQL files
    parent_dir = os.path.dirname(script_dir)
    
    # -----------------------------------------------------
    # 1) Run SQL queries on the SQLite database
    # -----------------------------------------------------
    db_path = os.path.join(parent_dir, "events.db")
    sql_path = os.path.join(parent_dir, "data.sql")
    
    # Get data from database
    df = get_data_from_database(db_path, sql_path)

    # -----------------------------------------------------
    # 2) Save the data to a CSV file
    # -----------------------------------------------------
    csv_path = os.path.join(script_dir, "wbr_data.csv")
    save_data_to_csv(df, csv_path)
    print(f"Data saved to {csv_path}")
    
    # -----------------------------------------------------
    # 3) Create a visualization and save it
    # -----------------------------------------------------
    chart_image_path = os.path.join(script_dir, "WBR_Visualization_Chart.png")
    pivot_df, _ = create_chart(df, chart_image_path)
    print(f"Chart saved to {chart_image_path}")
    
    # Get insights from the data
    insights = get_data_insights(df, pivot_df)
    
    # -----------------------------------------------------
    # 4) Send email with the chart attached and embedded
    # -----------------------------------------------------
    # Check if --send-email flag is provided
    send_email_flag = "--send-email" in sys.argv
    
    # If not provided as a flag, ask the user
    if not send_email_flag:
        send_email_flag = input("Do you want to send the email now? (yes/no): ").lower().strip() == 'yes'
    
    if send_email_flag:
        # Get email credentials
        credentials = get_email_credentials(has_config, config if has_config else None)
        
        # Create email message
        msg = create_email_message(credentials, pivot_df, insights, chart_image_path, csv_path)
        
        # Send the email
        send_email(credentials, msg)
    else:
        print("\nEmail sending skipped.")
        
        # Just show the email content that would have been sent
        print("\nEmail HTML content (preview):")
        email_html = """
        <html>
            <body>
                <p>Hello team,</p>
                <p>Please find below the updated chart from our WBR:</p>
                <p><img src="cid:chart_image" alt="WBR Chart" /></p>
                <p>Best regards,<br/>Automated Bot</p>
            </body>
        </html>
        """
        print(email_html)
    
    print("\nScript completed successfully!")

if __name__ == "__main__":
    main() 