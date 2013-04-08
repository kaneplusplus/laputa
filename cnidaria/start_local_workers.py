import os

def start_local_workers(nw=1, key="testkey", host="localhost", port=6379, 
  db=0, init_string=''):
  rs='''
import argparse
from Worker import *
w = Worker('KEY', 'HOST', PORT, DB)
w.service()
'''
  rs=rs.replace("KEY", key).replace("HOST", host).replace("PORT", 
    str(port)).replace("DB", str(db))
  rs=init_string+"\n"+rs
  for i in range(nw):
    os.system("python -c \"" + rs + "\" &")
  
