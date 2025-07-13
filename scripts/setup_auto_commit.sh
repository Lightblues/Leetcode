#!/bin/bash

# Set up auto commit cron job
# This script will create a cron job that runs auto_commit.sh periodically

# Get the absolute path of the current script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_NAME="$(basename "$(dirname "$SCRIPT_DIR")")"
echo "> Script directory: $SCRIPT_DIR"

# Check if auto_commit.sh exists and is executable
if [ ! -x "$SCRIPT_DIR/auto_commit.sh" ]; then
    echo "Error: $SCRIPT_DIR/auto_commit.sh does not exist or is not executable"
    exit 1
fi

# Create temporary crontab file
TEMP_CRONTAB=$(mktemp)
crontab -l > "$TEMP_CRONTAB" 2>/dev/null

# Check if the cron job already exists
if grep -q "$SCRIPT_DIR/auto_commit.sh" "$TEMP_CRONTAB"; then
    echo "自动提交任务已经存在于crontab中。"
    rm "$TEMP_CRONTAB"
    exit 0
fi

# Add cron job to run every hour
# Redirect output to log file (~/tmp/auto_commit/$PROJECT_NAME.log)
OUTPUT_LOG="/tmp/auto_commit_$PROJECT_NAME.log"
mkdir -p "/tmp/auto_commit"
echo "0 * * * * $SCRIPT_DIR/auto_commit.sh >> $OUTPUT_LOG 2>&1" >> "$TEMP_CRONTAB"

# Apply new crontab
crontab "$TEMP_CRONTAB"
rm "$TEMP_CRONTAB"

echo "已设置自动提交任务，将每小时执行一次。"
echo "您可以通过运行 'crontab -l' 查看所有定时任务。"
echo "如需修改执行频率，请编辑crontab（运行 'crontab -e'）。"
