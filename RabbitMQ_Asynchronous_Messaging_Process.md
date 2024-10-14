# RabbitMQ Asynchronous Messaging Process

## Objective
Implement an asynchronous messaging system using RabbitMQ to send and receive 1,000,000 messages, demonstrating the power of message queues in handling large volumes of data efficiently.

## Prerequisites
- macOS operating system
- Python 3.x installed
- Homebrew package manager

## Steps

### 1. Install RabbitMQ
```bash
brew install rabbitmq
```

### 2. Start RabbitMQ Server
```bash
brew services start rabbitmq
```

### 3. Install Pika (Python client for RabbitMQ)
```bash
pip3 install pika
```

### 4. Create Producer Script (cmpe273send-1.py)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:42:51 2023

@author: user
"""

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message_count = 1000000
start_time = time.time()

for i in range(message_count):
    channel.basic_publish(exchange='', routing_key='hello', body=f'Message {i+1}')
    if (i+1) % 100000 == 0:
        print(f" [x] Sent {i+1} messages")

end_time = time.time()
print(f" [x] Sent {message_count} messages in {end_time - start_time:.2f} seconds")

connection.close()
```

### 5. Run Producer Script
```bash
python3 cmpe273send-1.py
```

Output:
```
[x] Sent 100000 messages
[x] Sent 200000 messages
[x] Sent 300000 messages
[x] Sent 400000 messages
[x] Sent 500000 messages
[x] Sent 600000 messages
[x] Sent 700000 messages
[x] Sent 800000 messages
[x] Sent 900000 messages
[x] Sent 1000000 messages
[x] Sent 1000000 messages in 27.96 seconds
```

### 6. Create Consumer Script (cmpe273receive-1.py)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 15:08:49 2023

@author: user
"""

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message_count = 0
start_time = time.time()

def callback(ch, method, properties, body):
    global message_count
    message_count += 1
    if message_count % 100000 == 0:
        print(f" [x] Received {message_count} messages")

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

end_time = time.time()
print(f" [x] Received a total of {message_count} messages in {end_time - start_time:.2f} seconds")

connection.close()
```

### 7. Run Consumer Script
```bash
python3 cmpe273receive-1.py
```

Output:
```
[*] Waiting for messages. To exit press CTRL+C
[x] Received 100000 messages
[x] Received 200000 messages
[x] Received 300000 messages
[x] Received 400000 messages
[x] Received 500000 messages
[x] Received 600000 messages
[x] Received 700000 messages
[x] Received 800000 messages
[x] Received 900000 messages
[x] Received 1000000 messages
^C [x] Received a total of 1000000 messages in 250.67 seconds
```

## Results and Analysis

1. **Producer Performance**: The producer script successfully sent 1,000,000 messages in 27.96 seconds, demonstrating high throughput in message production.

2. **Consumer Performance**: The consumer script successfully received and processed all 1,000,000 messages in 250.67 seconds. The longer processing time for the consumer is expected, as it involves more operations per message (receiving, counting, and potentially processing).

3. **Asynchronous Nature**: The significant difference in time between sending and receiving demonstrates the asynchronous nature of the system. Messages were quickly queued by the producer and then processed at the consumer's pace without blocking the producer.

4. **Scalability**: This setup shows how RabbitMQ can handle a large volume of messages, making it suitable for scalable, distributed systems.

5. **Reliability**: All 1,000,000 messages sent were successfully received, showcasing the reliability of RabbitMQ in message delivery.

## Conclusion

This implementation successfully demonstrates the use of RabbitMQ for asynchronous messaging. It highlights the system's ability to handle a high volume of messages efficiently, separating the concerns of message production and consumption. This decoupling allows for greater flexibility and scalability in distributed system architectures.

The asynchronous nature of the message queue allows the producer to quickly send messages without waiting for them to be processed, while the consumer can process messages at its own pace. This is particularly useful in scenarios where there might be spikes in message production or where message processing is time-consuming.

Overall, this exercise showcases the power and efficiency of using message queues like RabbitMQ in building robust, scalable, and distributed systems.