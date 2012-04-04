import numpy as np
from matplotlib import pyplot as plt

# Load the data
filename = 'randomData.txt'
coord = np.dtype(dict(names=('x', 'y', 'z'), \
                      formats=('float', 'float', 'float') ) )
data = np.loadtxt(filename, dtype=coord, delimiter=',')

# create the subplots
f, axs = plt.subplots(2,2)
axs[0][0].plot(data['x'], data['y'], 'bo')
axs[0][1].plot(data['x'], data['z'], 'ro')
axs[1][0].plot(data['y'], data['z'], 'go')
axs[1][1].plot(data['x'], data['y'], 'bo', data['y'], data['z'], 'ro', \
               data['x'], data['z'], 'go' )
