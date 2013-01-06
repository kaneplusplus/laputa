#!/usr/bin/env python

import redis

if __name__ == '__main__':
  r = redis.StrictRedis()
  r.lpush("send", "message sent!")
  r.lpush("send", "message sent!")
  ack = r.brpop("ack")
  print("Received: "+ack[1])
  print("Destroying send key")
  r.delete("send")
