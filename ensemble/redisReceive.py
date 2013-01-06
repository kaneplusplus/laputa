#!/usr/bin/env python

import redis

if __name__ == '__main__':
  print("Waiting for message")
  r = redis.StrictRedis()
  message = r.brpop("send")
  r.lpush("ack", "message received")
  print(message)
#  print("Received: "+message)
  print("Deleting ack key")
  r.delete("ack")
