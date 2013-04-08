import redis, random
import cPickle as pickle
from util import *
 
class Coordinator:
  
  def __init__(self, key="testkey", host="localhost", port=6379, db=0, 
    timeout=30):
    self.key = key
    self.timeout = timeout
    self.r = redis.StrictRedis(self.host, self.port, self.db)

  def __init__(self, redis_handle, key="testkey", timeout=30):
    self.key=key
    self.timeout=timeout
    self.r=redis_handle

  def __del__(self):
    return self.r.delete(self.key)

  def publish_eval(self, expr):
    return self.remote_execute("eval", expr)

  def publish_exec(self, expr):
    return self.remote_execute("exec", expr)

  def publish_get(self, expr):
    return self.remote_execute("get", expr)

  def publish_shutdown(self):
    self.remote_execute("shutdown", "")

  def remote_execute(self, pub_type, expr):
    # Generate a return queue name and a return queue counter so we know
    # how many responses we're getting
    rq=random_key()

    # The worker queue tells us how many workers are working.
    rqw=rq+".worker"

    # Publish the job ot the listening workers.
    self.r.publish(self.key, pickle.dumps(publish_packet(pub_type,expr,rq,rqw)))

    # Note that the following may need to accomodate "lazy workers" that
    # are active but take too long to return a value.

    # Make sure we get into the while loop.
    resp=[]
    if pub_type != "shutdown":
      active_workers = 1
      while (active_workers > 1) or self.r.llen(rq):
        rv=self.r.brpop(rq, self.timeout)
        if (rv != None):
          resp.append(pickle.loads(rv[1]))
          active_workers = int(self.r.get(rqw))
      
      # Clean-up.
      self.r.delete(rqw)
      self.r.delete(rq)

    return resp
      
  def send_exec(self, expr):
    self.r.lpush(self.key, pickle.dumps(exec_packet(expr)))

  def send_eval(self, expr):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(eval_packet(expr, returnKey)))
    ret = pickle.loads(self.r.brpop(return_key, timeout)[1])
    self.r.delete(return_key)
    return ret

  def get_value(self, val):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(get_packet(val, return_key)))
    ret = pickle.loads(self.r.brpop(return_key, timout)[1])
    self.r.delete(return_key)
    return ret

def verbose(s):
  if args.verbose:
    print(s)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-k", "--key", nargs=1, default="testkey",
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

  args = parse_args() 
  if (not args.key):
    raise Exception("A worker queue key must be specified")

  verbose(args.key)
  verbose(args.host)
  verbose(args.port)
  verbose(args.db)
  rt = Coordinator(args.key, args.host, args.port, args.db)
  verbose("Tasker started.")
  
 
