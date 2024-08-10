# Makefile to copy files to an SSH server

# Define variables
SSH_HOST = rasp_3
SSH_PORT = 22  # Default SSH port
TARGET_DIR = /home/pi/led_strip_server

# Define the files to copy
FILES = *.sh *.py *.txt content

# Define the SCP command
SCP = scp -prP $(SSH_PORT)

# Define the SSH command
SSH = ssh -p $(SSH_PORT) $(SSH_HOST)

# Target to copy files
copy:
	@echo "Copying files to $(SSH_USER)@$(SSH_HOST):$(TARGET_DIR)"
	$(SCP) $(FILES) $(SSH_HOST):$(TARGET_DIR)

# Target to set up the environment on the server (optional)
setup:
	$(SSH) 'sudo pip install flask'

# Target to run the application on the server (optional)
run:
	$(SSH) 'cd $(TARGET_DIR) && sudo python app.py'

install: setup
	@echo "Copying config file to $(SSH_USER)@$(SSH_HOST):$(TARGET_DIR)"
	$(SCP) config.json $(SSH_HOST):$(TARGET_DIR)
	$(SSH) 'cd $(TARGET_DIR) && sudo ./install.sh'

service_start:
	$(SSH) 'sudo systemctl start ledserver'

service_stop:
	$(SSH) 'sudo systemctl stop ledserver'

service_restart:
	$(SSH) 'sudo systemctl restart ledserver'

service_status:
	$(SSH) 'sudo systemctl status ledserver'

service_enable_on_system_start:
	$(SSH) 'sudo systemctl enable ledserver'

service_disable_on_system_start:
	$(SSH) 'sudo systemctl disable ledserver'

service_journal:
	$(SSH) 'sudo journalctl -u ledserver | tail -n 500'
