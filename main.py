import os
import re
import smtplib
import time
import logging
from email.mime.text import MIMEText

# Configuration for Email Alerts
EMAIL_CONFIG = {
    'smtp_server': 'localhost',
    'smtp_port': 25,
    'smtp_user': '',
    'smtp_password': '',
    'from_email': 'test_user@test.com',
    'to_email': 'recipient@test.com'
}

# Log File Paths
LOG_PATHS = [
    '/var/log/auth.log',  # Adjust as needed
    '/var/log/syslog',    # Adjust as needed
]

# Alert Patterns to Scan For
ALERT_PATTERNS = [
    r'failed login',
    r'unauthorized access',
    r'privilege escalation',
    r'malware detected'
]

# Set up logging for the service
logging.basicConfig(
    filename='/var/log/monitorzer_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_log_file(file_path):
    """
    Reads a log file and returns log lines.
    """
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        logging.error(f"Error reading log file {file_path}: {e}")
        return []

def check_for_alerts(log_lines):
    """
    Scans log lines for specific alert patterns defined in ALERT_PATTERNS.
    """
    alerts = []
    for line in log_lines:
        for pattern in ALERT_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                alerts.append(line)
    return alerts

def send_email_alert(subject, body):
    """
    Sends email alerts using the SMTP server configuration.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['from_email']
    msg['To'] = EMAIL_CONFIG['to_email']

    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            if EMAIL_CONFIG['smtp_user'] and EMAIL_CONFIG['smtp_password']:
                server.login(EMAIL_CONFIG['smtp_user'], EMAIL_CONFIG['smtp_password'])
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def monitor_logs():
    """
    Monitors the specified log files and triggers alerts if patterns are detected.
    """
    try:
        alerts = []

        for log_path in LOG_PATHS:
            logs = read_log_file(log_path)
            alerts.extend(check_for_alerts(logs))

        if alerts:
            alert_body = '\n'.join(alerts)
            send_email_alert('Security Alert', alert_body)
            logging.info(f"Alerts found and email sent: {len(alerts)} alerts.")

    except Exception as e:
        logging.error(f"Error in monitor_logs: {e}")

if __name__ == "__main__":
    while True:
        monitor_logs()
        logging.info("Waiting before next scan...")
        time.sleep(60)  # Check logs every 60 seconds
