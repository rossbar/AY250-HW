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
# Initialize plot
fig = figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
# Plot execution times
ax1.loglog( simDomain, serialAry[:,2], 'b-o', label='Serial')
ax1.loglog( simDomain, multiAry[:,2], 'g-o', label='Multiprocessing')
ax1.loglog( simDomain, ipAry[:,2], 'y-o', label='IPcluster')
# Plot execution rates
ax2.semilogx( simDomain, serialAry[:,3], 'b--.')#, label='Serial')
ax2.semilogx( simDomain, multiAry[:,3], 'g--.')#, label='Multiprocessing')
ax2.semilogx( simDomain, ipAry[:,3], 'y--.')#, label='IPcluster')
# Decorate plot
ax1.set_title('Comparison of Parallel Execution Times with\n%s Processor'%proc )
ax1.set_xlabel('# of Darts')
ax1.set_ylabel('Log(Execution Time) [s], Solid Line')
ax2.set_ylabel('Simulation Rate (Darts/Sec) - Dashed Line')
ax1.legend(loc='upper left')
show()
