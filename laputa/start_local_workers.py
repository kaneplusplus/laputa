import os

def start_local_workers(nw=1, key="testkey", host="localhost", port=6379, 
  db=0, init_string='', path="", verbose=False):
  rs='''
import argparse
from laputa import Worker
w = Worker('KEY', 'HOST', PORT, DB, VERBOSE)
w.service()
'''
  rs=rs.replace("KEY", key).replace("HOST", host).replace("PORT", 
    str(port)).replace("DB", str(db)).replace("VERBOSE", str(verbose))
  rs=init_string+"\n"+rs
  for i in range(nw):
    os.system(path+"python -c \"" + rs + "\" &")
  
