#!/usr/bin/env python

from __future__ import print_function

import argparse, redis, sys

import cPickle as pickle

def warning(s):
  print("Warning: "+s+"\n", file=sys.stderr)

def verbose(s):
  if args.verbose:
    print(s)

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--key", nargs=1, default="testkey",
    help="The key to subscribe to commands on")
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
    raise(Exception("A key to the subscribe channel must be specified"))

  r = redis.StrictRedis(host=args.host, port=args.port, db=args.db)
  verbose("Connected to redis server")

  # It may be a good idea to add a timeout to the listener.
  ps = r.pubsub()
  print("subscribing on "+args.key)
  ps.subscribe(args.key)

  # We'll go until we get the signal to shutdown.
  for item in ps.listen(): 
    if item['type'] == 'message':
      packet = pickle.loads(item['data'])
      
      if packet['type'] == 'shutdown':
        print("Shutdown message received")

      else:
        # Increment the return queue worker count. 
        print("incrementing " + packet['rqw'])
        r.incr(packet['rqw'])

        verbose("Eval packet received")
        rv=None
        try:
          if packet['type'] == 'eval':
            print("eval packet")
            rv = eval(packet['payload'])
          elif packet['type'] == 'exec':
            print("exec packet")
            exec(packet['payload'])
            rv = True
          elif packet['type'] == 'get':
            print("get packet")
            rv = locals()[packet['payload']]
        except Exception as e:
          rv = e
        print("Pushing new packet onto "+packet['rq'])
        print(rv)
        r.lpush(packet['rq'], pickle.dumps(rv))

        # Decrement the return worker count and continue with the loop.
        print("decrementing " + packet['rqw'])
        r.decr(packet['rqw'])

'''
  packet = pickle.loads( r.brpop(args.key[0])[1] )
  print(packet)
  while packet['type'] != 'shutdown':
    print("message received")
    if packet['type'] == 'exec':
      verbose("Executing command "+packet['payload'])
      exec(packet['payload'])

    elif packet['type'] == 'eval':
      # Need to add exception catching in case an assignment is made
      # in the eval string.
      ret = eval(packet['payload'])
      r.lpush(packet['rq'], pickle.dumps(ret))

    elif packet['type'] == 'get':
      r.lpush(packet['rq'], pickle.dumps(locals()[packet['payload']]))

    packet = pickle.loads(r.brpop(args.key[0])[1])
'''
