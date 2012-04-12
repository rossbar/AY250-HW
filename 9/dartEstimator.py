from random import uniform
from math import sqrt
from time import time

def serialPiEstimator(numDarts):
  '''Given a number of darts specified by the user, use monte-carlo methods to
     estimate the value of pi using a simple rejection method (no var.-red.). 
     This is the serial implementation. Returns the approximation, number of
     darts, the execution time, and the darts/time.'''
  numDartsInCircle = 0
  
  # Start execution loop
  start = time()
  for i in range(numDarts):
    x, y = uniform(0,1), uniform(0,1)
    if sqrt( (x - 0.5)**2 + (y - 0.5)**2 ) <= 0.5: numDartsInCircle += 1
  end = time()
  totalTime = end - start # In seconds

  # Estimate pi
  piProx = 4 * numDartsInCircle / float( numDarts )
  return piProx, numDarts, totalTime, numDarts/totalTime
