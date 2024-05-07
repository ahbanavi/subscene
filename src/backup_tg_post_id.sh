#!/bin/bash

# Set SSH and database credentials (replace with your actual credentials)
SSH_HOST="server_ip_or_hostname"
SSH_USER="your_username"
SSH_PORT="22"  # Default SSH port, change if needed
USER="your_mysql_username"
PASSWORD="your_mysql_password"
DB="subscene"

# Get current timestamp for backup filename
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)

ssh -o StrictHostKeyChecking=no -p $SSH_PORT $SSH_USER@$SSH_HOST "mysql -h localhost -u $USER -p$PASSWORD $DB -e \"SELECT id, tg_post_id FROM all_subs WHERE tg_post_id IS NOT NULL\"" > backup_all_subs_${TIMESTAMP}.sql

# Choose one of the above commented options based on your setup

echo "Backup completed at $TIMESTAMP"
