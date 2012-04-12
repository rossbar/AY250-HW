import numpy as np
import dartEstimator

# Evaluate the different methods and store their results
simDomain = np.logspace(1,7,7)
serialData = []
multiproc = []
ipParData = []
for point in simDomain:
  point = int(point)
  serialData.append( dartEstimator.serialEstimator( point ) )
  multiproc.append( dartEstimator.multiProcessingEstimator( point ) )
  ipParData.append( dartEstimator.ipythonParEstimator( point ) )

# Plotting
from matplotlib.pyplot import *
from os import uname
# Get appropriate cpu setup
comp = uname()[1]
if comp == 'ross-desktop': proc = 'AMD Phenom Quad Core - 3.4 GHz'
elif comp == 'ross-LBL': proc = 'Intel i7 (8 Core) - 2.4 GHz'
# Convert to array for slice indexing
serialAry = np.array(serialData)
multiAry = np.array(multiproc)
ipAry = np.array(ipParData)
# Plot
fig, ax = subplots(1, 1, sharex=True)
ax.loglog( simDomain, serialAry[:,2], 'b-o', label='Serial')
ax.loglog( simDomain, multiAry[:,2], 'g-o', label='Multiprocessing')
ax.loglog( simDomain, ipAry[:,2], 'y-o', label='IPcluster')
ax.set_title('Comparison of Parallel Execution Times with\n%s Processor'%proc )
ax.set_xlabel('# of Darts')
ax.set_ylabel('Log(Execution Time) [s], Solid Line')
ax.legend(loc='upper left')
show()
