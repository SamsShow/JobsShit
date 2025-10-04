#!/bin/bash

# Navigate to the bot directory
cd "$(dirname "$0")"

# Start the bot in the background with nohup
echo "🚀 Starting Telegram Job Tracker Bot..."
nohup python3 job_tracker_bot.py > bot.log 2>&1 &

# Save the process ID
echo $! > bot.pid

echo "✅ Bot started successfully!"
echo "📝 Process ID: $(cat bot.pid)"
echo "📋 Logs: bot.log"
echo ""
echo "To stop the bot, run: ./stop_bot.sh"


