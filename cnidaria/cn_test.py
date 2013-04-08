import redis, time
from Coordinator import *
from start_local_workers import *

# Start 3 local workers on this machine.
start_local_workers(1)

# Make sure the workers are spawned and waiting for jobs. They can't receive
# a published before they exist. We'll give them a second to get started.
time.sleep(1)

r = redis.StrictRedis(host="localhost", port=6379, db=0)

# Start the coordinator.
c = Coordinator(r)

# An eval is an expression or a function call that returns something.
a = c.publish_eval("4*3")

# An exec should have assignments in it.
c.publish_exec("a = 3+4")

# And then it can be retrieved.
c.publish_get("a")

# Now shut down the workers.
c.publish_shutdown()

