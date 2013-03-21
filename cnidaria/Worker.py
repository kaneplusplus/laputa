import redis
import cPickle as pickle

class Worker:

  def __init__(self, key, host="localhost", port=6379, db=0):
    self.key=key
    self.host=host
    self.port=port
    self.db=db
    self.r = redis.StrictRedis(self.host, self.port, self.db)
    # The environment where evals and exec's will take place.
    self.env = {}

  def service(self):
    ps = self.r.pubsub()
    ps.subscribe(self.key)
  
    # We'll go until we get the signal to shutdown.
    for item in ps.listen(): 
      if item['type'] == 'message':
        packet = pickle.loads(item['data'])
        
        if packet['type'] == 'shutdown':
          print("Shutdown message received")
          return True

        else:
          # Increment the return queue worker count. 
         # print("incrementing " + packet['rqw'])
          self.r.incr(packet['rqw'])

          rv=None
          try:
            if packet['type'] == 'eval':
              #print("eval packet")
              rv = eval(packet['payload'], self.env)
            elif packet['type'] == 'exec':
              #print("exec packet")
              exec(packet['payload'], self.env)
              rv = True
            elif packet['type'] == 'get':
              #print("get packet")
              rv = self.env[packet['payload']]
          except Exception as e:
            rv = e
          #print("Pushing new packet onto "+packet['rq'])
          #print(rv)
          self.r.lpush(packet['rq'], pickle.dumps(rv))

          # Decrement the return worker count and continue with the loop.
          #print("decrementing " + packet['rqw'])
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

    
