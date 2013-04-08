import os

def clear_env():
# Kill all python processes on the machine.
  rs = '''ps aux | grep python | awk '{print $2}' | xargs kill
redis-cli flushdb
redis-cli flushall
'''
  os.system(rs)
