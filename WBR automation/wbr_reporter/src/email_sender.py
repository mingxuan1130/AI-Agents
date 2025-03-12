import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from datetime import datetime
import getpass

def get_email_credentials(has_config, config=None):
    """
    Get email credentials either from config or by asking the user.
    
    Args:
        has_config (bool): Whether a config file is available
        config (module, optional): Config module with email settings
        
    Returns:
        dict: Dictionary containing email credentials and settings
    """
    if has_config and config and hasattr(config, 'SENDER_EMAIL') and hasattr(config, 'SENDER_PASSWORD') and hasattr(config, 'RECIPIENT_EMAIL'):
        if config.SENDER_EMAIL and config.SENDER_PASSWORD and config.RECIPIENT_EMAIL:
            credentials = {
                'sender_email': config.SENDER_EMAIL,
                'recipient_email': config.RECIPIENT_EMAIL,
                'password': config.SENDER_PASSWORD,
                'smtp_server': config.SMTP_SERVER,
                'smtp_port': config.SMTP_PORT,
                'subject_prefix': config.EMAIL_SUBJECT_PREFIX,
                'sender_name': config.SENDER_NAME
            }
            print(f"Using email settings from config.py")
            return credentials
        else:
            print("Email settings in config.py are incomplete.")
    
    # If no config or incomplete, ask user
    print("Please enter email details:")
    credentials = {
        'sender_email': input("Enter your email address: "),
        'recipient_email': input("Enter recipient email address: "),
        'password': getpass.getpass("Enter your email password or app password: "),
        'smtp_server': "smtp.gmail.com",  # Default to Gmail
        'smtp_port': 587,
        'subject_prefix': "Weekly Business Review (WBR) Chart",
        'sender_name': "Automated WBR System"
    }
    
    return credentials

def create_email_message(credentials, pivot_df, insights, chart_path, csv_path):
    """
    Create an email message with the chart and data insights.
    
    Args:
        credentials (dict): Email credentials and settings
        pivot_df (pandas.DataFrame): Pivoted DataFrame used for visualization
        insights (dict): Data insights dictionary
        chart_path (str): Path to the chart image
        csv_path (str): Path to the CSV data file
        
    Returns:
        MIMEMultipart: Email message object
    """
    # Create email message
    msg = MIMEMultipart('related')
    msg['Subject'] = f'{credentials["subject_prefix"]} - {datetime.now().strftime("%Y-%m-%d")}'
    msg['From'] = f'{credentials["sender_name"]} <{credentials["sender_email"]}>'
    msg['To'] = credentials['recipient_email']
    
    # Create the HTML part
    html_part = MIMEMultipart('alternative')
    
    # Create email content
    email_html = f"""
    <html>
        <body>
            <p>Hello team,</p>
            <p>Please find below the updated chart from our Weekly Business Review:</p>
            <p><img src="cid:chart_image" alt="WBR Chart" width="800" /></p>
            <p>The data shows event counts by category from {insights['date_range'][0]} to {insights['date_range'][1]}.</p>
            <p>Key observations:</p>
            <ul>
                <li>Total events: {insights['total_events']}</li>
                <li>Most common category: {insights['most_common_category']['name']} 
                   ({insights['most_common_category']['count']} events)</li>
                <li>Date with most events: {insights['busiest_date']['date']} 
                   ({insights['busiest_date']['count']} events)</li>
            </ul>
            <p>The full dataset is attached as a CSV file for your reference.</p>
            <p>Best regards,<br/>{credentials['sender_name']}</p>
        </body>
    </html>
    """
    
    html_content = MIMEText(email_html, 'html')
    html_part.attach(html_content)
    msg.attach(html_part)
    
    # Attach the chart image and reference it in the HTML
    with open(chart_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<chart_image>')
        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(chart_path))
        msg.attach(img)
    
    # Attach the CSV file
    with open(csv_path, 'rb') as csv_file:
        csv_attachment = MIMEText(csv_file.read().decode('utf-8'), 'csv')
        csv_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(csv_path))
        msg.attach(csv_attachment)
    
    return msg

def send_email(credentials, msg):
    """
    Send an email using the provided credentials and message.
    
    Args:
        credentials (dict): Email credentials and settings
        msg (MIMEMultipart): Email message to send
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Set up the SMTP server
        print("\nConnecting to email server...")
        
        server = smtplib.SMTP(credentials['smtp_server'], credentials['smtp_port'])
        server.starttls()  # Secure the connection
        
        # Login to email server
        server.login(credentials['sender_email'], credentials['password'])
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        print("\nTroubleshooting tips:")
        print("1. If using Gmail, make sure you've created an App Password if you have 2-factor authentication enabled.")
        print("2. Check your internet connection.")
        print("3. Verify your email credentials are correct.")
        print("4. Make sure your email provider allows SMTP access.")
        return False 