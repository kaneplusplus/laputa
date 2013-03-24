import os

def start_local_workers(nw=1, key="testkey", host="localhost", port=6379, 
  db=0, init_string=''):
  rs = str("import argparse, cnidaria\n" + init_string + "\n" +
    "w = cnidaria.Worker ('" + key + "', '" + host + "', " + str(port) +
    ", " + str(db) + ")\n" + "w.service()")
  for i in range(nw):
    os.system("python -c \"" + rs + "\" &")
  
