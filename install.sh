#!/bin/bash

SERVICE_NAME="ledserver"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
WORKING_DIR="/home/pi/led_strip_server"
PYTHON_EXEC="/usr/bin/python3"
SCRIPT_NAME="app.py"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Create systemd service file
echo "Creating systemd service file at ${SERVICE_FILE}..."

cat <<EOL > ${SERVICE_FILE}
[Unit]
Description=LED Server
After=network.target

[Service]
ExecStart=${PYTHON_EXEC} ${WORKING_DIR}/${SCRIPT_NAME}
WorkingDirectory=${WORKING_DIR}
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to apply the new service
echo "Reloading systemd..."
systemctl daemon-reload

# Start the new service
echo "Starting ${SERVICE_NAME} service..."
systemctl start ${SERVICE_NAME}

# Enable the service to start on boot
echo "Enabling ${SERVICE_NAME} service to start on boot..."
systemctl enable ${SERVICE_NAME}

echo "Installation complete. You can check the status of the service using:"
echo "sudo systemctl status ${SERVICE_NAME}"