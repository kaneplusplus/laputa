#!/usr/bin/env python

from __future__ import print_function

import argparse, redis, string, random

import cPickle as pickle
  
def cnrPacket(commandString):
  return {'type' : 'cnr', 'payload' : commandString, 'rq' : None}

def funPacket(commandString, rq):
  return {'type' : 'fun', 'payload' : commandString, 'rq' : rq}

def getPacket(varString, rq):
  return {'type' : 'get', 'payload' : varString, 'rq' : rq}

def random_key(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for x in range(size))


class RedisTasker:
  
  def __init__(self, key, host="localhost", port=6379, db=0):
    self.key = key
    self.host = host
    self.port = port
    self.db = db
    self.r = redis.StrictRedis(self.host, self.port, self.db)

  def sendCommand(self, command):
    self.r.lpush(self.key, pickle.dumps(cnrPacket(command)))

  def functionCall(self, functionCall):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(funPacket(val, returnKey)))
    ret = pickle.loads(self.r.brpop(returnKey)[1])
    self.r.delete(returnKey)
    return ret

  def getValue(self, val):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(getPacket(val, returnKey)))
    ret = pickle.loads(self.r.brpop(returnKey)[1])
    self.r.delete(returnKey)
    return ret

def warning(s):
  print("Warning: "+s+"\n", file=sys.stderr)

def verbose(s):
  if args.verbose:
    print(s)

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--key", nargs=1, default=None,
    help="The key to send the command on")
  parser.add_argument("-o", "--host", nargs=1, default="localhost",
    help="The host to send the commands to")
  parser.add_argument("-p", "--port", nargs=1, default=6379, type=int,
    help="The port to start the server on")
  parser.add_argument("-d", "--db", nargs=1, default=0, type=int,
    help="The database ID")
  parser.add_argument("-v", "--verbose", action="store_const", const=True,
    default=False)
  return parser.parse_args()

if __name__=='__main__':

  args = parseArgs() 
  if (not args.key):
    raise(Exception("A worker queue key must be specified"))

  print(args.key[0])
  print(args.host)
  print(args.port)
  print(args.db)
  rt = RedisTasker(args.key[0], args.host, args.port, args.db)
  verbose("Tasker started.")

  print("Sending cnr command")
  rt.sendCommand("a = 4*3+2345")
  returnValue = rt.getValue("a")
  print(returnValue)
  
#  r.delete(args.key)
 
