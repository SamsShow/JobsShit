#!/bin/bash

# Navigate to the bot directory
cd "$(dirname "$0")"

if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    echo "🛑 Stopping bot (PID: $PID)..."
    kill $PID 2>/dev/null
    rm bot.pid
    echo "✅ Bot stopped!"
else
    echo "❌ No bot.pid file found. Bot may not be running."
    echo "Looking for python processes..."
    pkill -f "job_tracker_bot.py"
fi


