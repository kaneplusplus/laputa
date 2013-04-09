import os

def clear_env():
# Kill all python processes on the machine.
  rs = '''redis-cli flushdb
redis-cli flushall
ps aux | grep python | awk '{print $2}' | xargs kill
'''
  os.system(rs)
