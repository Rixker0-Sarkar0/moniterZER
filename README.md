# Monitoring and Alerting System

## Introduction

This project helps you monitor log files and send email alerts when specific patterns are detected. It’s useful for keeping an eye on your system logs for important events.

## What You Need

- **Python 3.x**: Ensure Python 3.x is installed on your machine.
- **Email Server**: You need an email server to send alerts. You can use a local server like `hMailServer` or any other SMTP server.

## Setting Up the System

### 1. Prepare Your Environment

1. **clone this repo**

2. **Create a Directory for the Script**

    Open a terminal and run:

    ```bash
    mkdir ~/monitorzer
    cd ~/monitorzer
    ```

3. **Make the Script Executable**

    Run the following command to make the script executable:

    ```bash
    chmod +x monitorzer.py
    ```

### 2. Configure the Script

- **Edit Email Settings**: Update the `EMAIL_CONFIG` section in the script with your SMTP server details and email addresses.
- **Set Log File Paths**: Modify `LOG_PATHS` if your log files are in different locations.
- **Define Alert Patterns**: Adjust `ALERT_PATTERNS` to include the patterns you want to search for.

### 3. Set Up the Script as a System Daemon

1. **Create a Systemd Service File**

    Create a service file named `monitorzer.service` in the `/etc/systemd/system/` directory:

    ```bash
    sudo nano /etc/systemd/system/monitorzer.service
    ```

    Add the following content to the file:

    ```ini
    [Unit]
    Description=Monitorzer Log Monitoring Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/username/monitorzer/monitorzer.py
    Restart=always
    User=username
    Group=groupname

    [Install]
    WantedBy=multi-user.target
    ```

    Replace `username` and `groupname` with your actual username and group.

2. **Reload Systemd and Start the Service**

    Run the following commands to reload the systemd manager configuration and start the service:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start monitorzer.service
    ```

3. **Enable the Service to Start on Boot**

    To ensure the service starts automatically on system boot, run:

    ```bash
    sudo systemctl enable monitorzer.service
    ```

4. **Check the Service Status**

    To check the status of the service, use:

    ```bash
    sudo systemctl status monitorzer.service
    ```

## Troubleshooting

- **No Alerts**: Ensure that your log files contain entries matching the alert patterns.
- **Email Issues**: Verify your email server settings and check the script log for any errors.
- **Service Issues**: Check the service status with `systemctl status monitorzer.service` for any errors.

## Conclusion

This guide helps you set up a monitoring and alerting system on Linux and configure it to run as a system daemon. If you encounter issues or need more help, refer to the script logs or consult further documentation on Python, systemd, and email configuration.
