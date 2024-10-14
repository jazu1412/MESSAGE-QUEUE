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