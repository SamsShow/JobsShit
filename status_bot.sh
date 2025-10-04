#!/bin/bash

# Navigate to the bot directory
cd "$(dirname "$0")"

echo "🔍 Checking bot status..."
echo ""

if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ Bot is RUNNING (PID: $PID)"
        echo ""
        echo "📊 Recent logs:"
        echo "─────────────────────────────────────"
        tail -n 10 bot.log
    else
        echo "❌ Bot is NOT running (stale PID file)"
        rm bot.pid
    fi
else
    if pgrep -f "job_tracker_bot.py" > /dev/null; then
        echo "⚠️  Bot appears to be running but no PID file found"
        echo "PID: $(pgrep -f job_tracker_bot.py)"
    else
        echo "❌ Bot is NOT running"
    fi
fi


