#!/usr/bin/env python

from __future__ import print_function

import argparse, redis

import cPickle as pickle

def warning(s):
  print("Warning: "+s+"\n", file=sys.stderr)

def verbose(s):
  if args.verbose:
    print(s)

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--key", nargs=1, default=None,
    help="The key to listen for commands on")
  parser.add_argument("-o", "--host", nargs=1, default="localhost",
    help="The host for the worker to connect to")
  parser.add_argument("-p", "--port", nargs=1, default=6379, type=int,
    help="The port for the worker to connect to")
  parser.add_argument("-d", "--db", nargs=1, default=0, type=int,
    help="The database ID for the worker to connect to")
  parser.add_argument("-v", "--verbose", action="store_const", const=True,
    default=False)
  return parser.parse_args()

if __name__=='__main__':

  args = parseArgs()
  if (not args.key):
    raise(Exception("A worker queue key must be specified"))

  r = redis.StrictRedis(host=args.host, port=args.port, db=args.db)
  verbose("Connected to redis server")

  # A packet is a dictionary with a key with:
  #   type:
  #     shutdown - shutdown the client
  #     cnr      - execute a command with no return (exec)
  #     fun      - execute a function and return on a queue (eval)
  #     get      - get a variable
  #   payload - the command to execute
  #   rq - the key for the return queue
  packet = pickle.loads( r.brpop(args.key[0])[1] )
  while packet['type'] != 'shutdown':
    if packet['type'] == 'cnr':
      verbose("Executing command "+packet['payload'])
      exec(packet['payload'])
    if packet['type'] == 'fun':
      # Need to add exception catching in case an assignment is made
      # in the eval string.
      ret = eval(packet['payload'])
      r.lpush(packet['rq'], pickle.dumps(ret))
    if packet['type'] == 'get':
      r.lpush(packet['rq'], pickle.dumps(locals()[packet['payload']]))
    packet = pickle.loads(r.brpop(args.key)[1])

  verbose("Shutdown packet received. Worker shutting down.")

