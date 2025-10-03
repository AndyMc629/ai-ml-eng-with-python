#!/bin/bash
set -euo pipefail

# Start FastAPI dev server in the background
fastapi dev basic_fastapi_agent.py --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait a few seconds for the server to be ready
echo "Waiting for FastAPI server to start..."
sleep 5

# Send test request
curl -X 'POST' \
  'http://127.0.0.1:8000/stream' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Tell me the time, but then take that time and make it an integer, take that integer and then map the individual numbers to a letter of the alphabet, then count how many a'\''s there are in that final word. Show your working."
}'

# Kill the server afterwards
kill $SERVER_PID