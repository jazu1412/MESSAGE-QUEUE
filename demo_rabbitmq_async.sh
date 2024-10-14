#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if RabbitMQ is installed
if ! command_exists rabbitmq-server; then
    echo "RabbitMQ is not installed. Please install it first."
    exit 1
fi

# Check if Python is installed
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "pip3 is not installed. Please install it first."
    exit 1
fi

# Install pika if not already installed
pip3 install pika

# Start RabbitMQ server
echo "Starting RabbitMQ server..."
brew services start rabbitmq
sleep 5  # Wait for RabbitMQ to fully start

# Run the producer script
echo "Running producer script..."
python3 cmpe273send-1.py &
PRODUCER_PID=$!

# Wait for the producer to finish
wait $PRODUCER_PID

# Run the consumer script
echo "Running consumer script..."
python3 cmpe273receive-1.py &
CONSUMER_PID=$!

# Wait for user input to stop the consumer
echo "Press Enter to stop the consumer..."
read

# Stop the consumer
kill $CONSUMER_PID

# Stop RabbitMQ server
echo "Stopping RabbitMQ server..."
brew services stop rabbitmq

echo "Demo completed."