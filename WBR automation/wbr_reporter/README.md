# Weekly Business Review (WBR) Automation

## Introduction

The Weekly Business Review (WBR) Automation tool is a Python-based solution designed to streamline the process of generating and distributing regular business reports. This tool automates the entire workflow from data extraction to report generation and email distribution, saving time and ensuring consistency in reporting.

### Key Features

- **Automated Data Extraction**: Queries a SQLite database to extract event data
- **Data Visualization**: Creates stacked bar charts to visualize event trends by category and date
- **Automated Reporting**: Generates and sends email reports with embedded charts and data insights
- **Modular Design**: Organized into separate modules for database operations, visualization, and email sending
- **Configurable**: Easily customizable through a configuration file

## Project Structure

```
WBR automation/
├── events.db                  # SQLite database with event data
├── data.sql                   # SQL query for data extraction
└── wbr_reporter/              # Main project directory
    ├── src/                   # Source code package
    │   ├── __init__.py        # Package initialization
    │   ├── database.py        # Database operations module
    │   ├── visualization.py   # Data visualization module
    │   └── email_sender.py    # Email functionality module
    ├── config.py              # Email and configuration settings
    ├── wbr_automation.py      # Main script
    ├── wbr_data.csv           # Generated data file (output)
    └── WBR_Visualization_Chart.png  # Generated chart (output)
```

## Setup

### Prerequisites
- Python 3.6+
- Required Python packages:
  ```
  pip install pandas matplotlib
  ```

### Installation
1. Clone or download this repository
2. Navigate to the project directory
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration
1. Edit the `config.py` file to set up your email credentials:
   ```python
   SENDER_EMAIL = "your.email@example.com"
   SENDER_PASSWORD = "your-app-password"
   RECIPIENT_EMAIL = "recipient@example.com"
   ```

2. For Gmail users:
   - If you have 2-factor authentication enabled:
     - Create an App Password at: Google Account > Security > App Passwords
     - Use this App Password in the config file
   - If you don't have 2-factor authentication:
     - Enable "Less secure app access" in your Google account settings

## Usage

### Basic Usage
Run the script:
```
python wbr_automation.py
```

The script will:
1. Query the SQLite database using the SQL in `data.sql`
2. Save the data to `wbr_data.csv`
3. Create a visualization chart and save it as `WBR_Visualization_Chart.png`
4. Ask if you want to send an email with the report

### Automated Email Sending
To automatically send the email without prompts:
```
python wbr_automation.py --send-email
```

### Scheduling
You can schedule this script to run automatically:

#### On macOS/Linux:
Add a crontab entry:
```
# Run every Monday at 8:00 AM
0 8 * * 1 cd /path/to/WBR\ automation/wbr_reporter && /usr/bin/python3 wbr_automation.py --send-email
```

#### On Windows:
Use Task Scheduler to run the script at your desired schedule.

## Customization

### Modifying the SQL Query
Edit the `data.sql` file to change what data is extracted from the database.

### Customizing the Visualization
Modify the `create_chart` function in `src/visualization.py` to change the chart appearance.

### Customizing the Email Template
Edit the `create_email_message` function in `src/email_sender.py` to customize the email content.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 