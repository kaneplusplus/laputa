import os

def startLocalWorkers(nw=1, key="testkey", host="localhost", port=6379, db=0):
  rs = str("import argparse, cnidaria\n" +
    "w = cnidaria.worker ('" + key + "', '" + host + "', " + str(port) +
    ", " + str(db) + ")\n" + "w.service()")
  for i in range(nw):
    os.system("python -c \"" + rs + "\" &")
  
