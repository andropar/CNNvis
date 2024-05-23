#!/bin/bash

# Function to stop child processes
stop_processes() {
  kill $python_pid $serve_pid
}

# Catch SIGINT and stop child processes
trap stop_processes SIGINT

# Start the first process
python /app/backend/app.py &
status=$?
python_pid=$!
if [ $status -ne 0 ]; then
  echo "Failed to start app.py: $status"
  exit $status
fi

# Start the second process
serve -s /app/frontend/build -l 5000 &
status=$?
serve_pid=$!
if [ $status -ne 0 ]; then
  echo "Failed to start npm: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  echo "Checking processes..."
done