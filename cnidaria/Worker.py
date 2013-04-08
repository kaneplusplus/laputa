from __future__ import print_function
import redis
import cPickle as pickle
from functools import partial
from util import *

class Worker:

  def __init__(self, key, host="localhost", port=6379, db=0, verbose=False):
    self.key=key
    self.host=host
    self.port=port
    self.db=db
    self.r = redis.StrictRedis(self.host, self.port, self.db)
    # The environment where evals and exec's will take place.
    self.env = {}
    self.guid = random_key()
    self.vprint = (print if verbose else lambda x: None)

  def service(self):
    ps = self.r.pubsub()
    ps.subscribe(self.key)
  
    # We'll go until we get the signal to shutdown.
    for item in ps.listen(): 

      if item['type'] == 'message':
        packet = pickle.loads(item['data'])
        
        if packet['type'] == 'shutdown':
          self.vprint("Shutdown message received")

        else:
          # Increment the return queue worker count. 
         # print("incrementing " + packet['rqw'])
          self.r.incr(packet['rqw'])

          rv=None
          try:
            if packet['type'] == 'eval':
              self.vprint("eval packet")
              self.vprint("'''")
              self.vprint(packet['payload'])
              self.vprint("'''")
              self.vprint("\n")
              rv = eval(packet['payload'], self.env)
            elif packet['type'] == 'exec':
              self.vprint("exec packet")
              self.vprint("'''")
              self.vprint(packet['payload'])
              self.vprint("'''")
              self.vprint("\n")
              exec(packet['payload'], self.env)
              rv = True
            elif packet['type'] == 'get':
              self.vprint("get packet")
              self.vprint("'''")
              self.vprint(packet['payload'])
              self.vprint("'''")
              self.vprint("\n")
              rv = self.env[packet['payload']]
          except Exception as e:
            self.vprint("Exception in packet processing")
            self.vprint(e)
            self.vprint("\n")
            rv = e
          self.r.lpush(packet['rq'], pickle.dumps( (self.guid, rv)) )

          # Decrement the return worker count and continue with the loop.
          self.r.decr(packet['rqw'])

def parse_args():
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

  args = parse_args()
  if (not args.key):
    raise(Exception("A key to the subscribe channel must be specified"))

  w = Worker(args.key, args.host, args.port, args.db)
  w.service()

