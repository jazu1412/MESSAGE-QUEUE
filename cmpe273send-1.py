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