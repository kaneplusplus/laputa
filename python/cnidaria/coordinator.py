import redis, random
import cPickle as pickle
 
def execPacket(expr, rq):
  return {'type':'exec', 'payload':expr, 'rq':rq}

def evalPacket(expr, rq):
  return {'type':'eval', 'payload':expr, 'rq':rq}

def shutdownPacket(expr, rq):
  return {'type':'shutdown'}

def publishPacket(pubType, expr, rq, rqw):
  return {'type':pubType, 'payload':expr, 'rq':rq, 'rqw':rqw}

def getPacket(varName, rq):
  return {'type':'get', 'payload':varName, 'rq':rq}

def random_key(size=6, chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
  return ''.join(random.choice(chars) for x in range(size))


class coordinator:
  
  def __init__(self, key="testkey", host="localhost", port=6379, db=0, 
    timeout=30):
    self.key = key
    self.host = host
    self.port = port
    self.db = db
    self.timeout = timeout
    self.r = redis.StrictRedis(self.host, self.port, self.db)

  def __del__(self):
    return self.r.delete(self.key)

  def publishEval(self, expr):
    return self.remoteExecute("eval", expr)

  def publishExec(self, expr):
    return self.remoteExecute("exec", expr)

  def publishGet(self, expr):
    return self.remoteExecute("get", expr)

  def publishShutdown(self):
    self.remoteExecute("shutdown", "")

  def remoteExecute(self, pubType, expr):
    # Generate a return queue name and a return queue counter so we know
    # how many responses we're getting
    rq=random_key()

    # The worker queue tells us how many workers are working.
    rqw=rq+".worker"

    # Publish the job ot the listening workers.
    self.r.publish(self.key, pickle.dumps(publishPacket(pubType,expr,rq,rqw)))
    resp=[]

    # Note that the following may need to accomodate "lazy workers" that
    # are active but take too long to return a value.

    # Make sure we get into the while loop.
    if pubType != "shutdown":
      activeWorkers = 1
      while activeWorkers or self.r.llen(rq):
        rv=self.r.brpop(rq, self.timeout)
        if rv:
          resp.append(pickle.loads(rv[1]))

        activeWorkers = int(self.r.get(rqw))
      
      # Clean-up.
      self.r.delete(rqw)
      self.r.delete(rq)

    return resp
      

  def sendExec(self, expr):
    self.r.lpush(self.key, pickle.dumps(execPacket(expr)))

  def sendEval(self, expr):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(evalPacket(expr, returnKey)))
    ret = pickle.loads(self.r.brpop(returnKey, timeout)[1])
    self.r.delete(returnKey)
    return ret

  def getValue(self, val):
    returnKey = random_key()
    self.r.lpush(self.key, pickle.dumps(getPacket(val, returnKey)))
    ret = pickle.loads(self.r.brpop(returnKey, timout)[1])
    self.r.delete(returnKey)
    return ret

def verbose(s):
  if args.verbose:
    print(s)

def parseArgs():
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

  args = parseArgs() 
  if (not args.key):
    raise(Exception("A worker queue key must be specified"))

  verbose(args.key)
  verbose(args.host)
  verbose(args.port)
  verbose(args.db)
  rt = coordinator(args.key, args.host, args.port, args.db)
  verbose("Tasker started.")
  
 
