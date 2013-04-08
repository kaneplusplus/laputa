import random

def exec_packet(expr, rq):
  return {'type':'exec', 'payload':expr, 'rq':rq}

def eval_packet(expr, rq):
  return {'type':'eval', 'payload':expr, 'rq':rq}

def shutdown_packet(expr, rq):
  return {'type':'shutdown'}

def publish_packet(pubType, expr, rq, rqw):
  return {'type':pubType, 'payload':expr, 'rq':rq, 'rqw':rqw}

def get_packet(varName, rq):
  return {'type':'get', 'payload':varName, 'rq':rq}

def random_key(size=6, chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
  return ''.join(random.choice(chars) for x in range(size))

