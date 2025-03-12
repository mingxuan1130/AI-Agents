# Email Configuration Settings
# Fill in your email details below

# Sender email settings
SENDER_EMAIL = "your.email@example.com"  # Your email address
SENDER_PASSWORD = "your-app-password-here"  # Your email password or app password

# Recipient email settings
RECIPIENT_EMAIL = "recipient@example.com"  # Recipient's email address

# SMTP server settings (default is for Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email content settings
EMAIL_SUBJECT_PREFIX = "Weekly Business Review (WBR) Chart"
SENDER_NAME = "Automated WBR System"

"""
IMPORTANT NOTES FOR GMAIL USERS:
-------------------------------
1. If you have 2-factor authentication enabled on your Google account:
   - You need to create an "App Password" specifically for this script
   - Go to your Google Account > Security > App Passwords
   - Select "Mail" and your device, then generate and use that password here

2. If you don't have 2-factor authentication:
   - You need to enable "Less secure app access" in your Google account
   - Go to your Google Account > Security > Less secure app access
   - Turn on "Allow less secure apps"

3. For security, consider:
   - Using environment variables instead of hardcoding credentials
   - Using a dedicated email account for automation
   - Restricting access to this configuration file
""" 