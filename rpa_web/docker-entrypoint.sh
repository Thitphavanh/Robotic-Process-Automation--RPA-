#!/bin/bash
set -e

echo "🚀 Starting RPA Bot Manager..."

# Start Xvfb (Virtual Frame Buffer) for GUI automation
echo "📺 Starting Xvfb virtual display..."
Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &
export DISPLAY=:99

# Wait for Xvfb to start
sleep 2

echo "✅ Xvfb started on DISPLAY=$DISPLAY"

# Execute the main command
exec "$@"
