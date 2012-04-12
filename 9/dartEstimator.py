from random import uniform
from math import sqrt
from time import time
from multiprocessing import Pool, cpu_count
from IPython.parallel import Client

def estimatePi(numIn, total):
  return 4 * numIn / float(total)

def determineNumDartsInCircle(numDarts):
  '''Given the total number of darts, return what fraction were in the circle'''
  numDartsInCircle = 0
  for i in range(numDarts):
    x, y = uniform(0,1), uniform(0,1)
    if sqrt( (x - 0.5)**2 + (y - 0.5)**2 ) <= 0.5: numDartsInCircle += 1
  return numDartsInCircle

def serialEstimator(numDarts):
  '''Given a number of darts specified by the user, use monte-carlo methods to
     estimate the value of pi using a simple rejection method (no var.-red.). 
     This is the serial implementation. Returns the approximation, number of
     darts, the execution time, and the darts/time.'''
  
  # Start execution loop
  start = time()
  numDartsInCircle = determineNumDartsInCircle( numDarts )
  end = time()
  totalTime = end - start # In seconds

  return estimatePi(numDartsInCircle, numDarts), numDarts, totalTime,\
         numDarts/totalTime

def multiProcessingEstimator(numDarts):
  '''Does the same as the above function except attempts to split the number
     of darts into num_processors equivalent problems and use 
     multiprocessing.pool to map the load to num_processors # of procs'''
  # Determine the number of cores available
  numProc = cpu_count()
  # Divide the darts into even workloads among the cores
  ndiv = int(round(numDarts/numProc))
  # Run Execution loop
  start = time()
  p = Pool(numProc)
  result = p.map_async( determineNumDartsInCircle, [ndiv]*numProc )
  poolResult = result.get()
  numDartsInCircle = sum(poolResult)
  end = time()
  totalTime = end - start
  return estimatePi(numDartsInCircle, numDarts), numDarts, totalTime,\
         numDarts/totalTime

def ipythonParEstimator(numDarts):
  '''The third implementation of the code. From the top-level, it runs in an
     identical fashion as the multiprocessing function, except it relies on
     the parallel machinery built into IPython rather than an external module'''
  # Determine the number of cores available
  numProc = cpu_count()
  # Divide the darts into even workloads among the cores
  ndiv = int(round(numDarts/numProc))
  # Run Execution loop
  start = time()
  # Generate the client
  lc = Client()
  dview = lc[:]
  par = dview.map_async( determineNumDartsInCircle, [ndiv]*numProc )
  numDartsInCircle = sum( par.result )
  end = time()
  totalTime = end - start
  return estimatePi(numDartsInCircle, numDarts), numDarts, totalTime,\
         numDarts/totalTime
  
