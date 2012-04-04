import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def getData(filename):
  '''Load the data from the filename and return two lists of floats containing
     the x and y data'''
  f = open( filename, 'r' )
  lines = f.readlines()
  f.close()

  xdata = []
  ydata = []
  # Remove the comment line
  lines.pop(0)
  for line in lines:
    linedata = line.split('\t')
    # for each individual line, remove the trailing characters and convert
    # the values to floats
    for i in range(0,len(linedata)):
      linedata[i] = linedata[i].strip()
      linedata[i] = float( linedata[i] )
    xdata.append( linedata[0] )
    ydata.append( linedata[1] )
  return xdata, ydata

# Initialize the problem
path = r'Homework1_files/'
filenames = ['google_data.txt', 'ny_temps.txt', 'yahoo_data.txt']
labels = ['Google Stock Value', 'NY Mon. High Temp', 'Yahoo Stock Value']
formats = ['b-', 'r--', '-']
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
# Open each file, plot the data according to the formats and labels listed
# above
for i,name in enumerate(filenames):
  fullPath = path + name
  x, y = getData(fullPath)
  if 'Temp' in labels[i]:
    ax2.plot( x, y, formats[i], label=labels[i] )
  else:
    if 'Yahoo' in labels[i]:
      ax1.plot( x, y, color='purple', label=labels[i] )
    else:
      ax1.plot( x, y, formats[i], label=labels[i] )
#### Set some of the parameters to match the original picture closely
ax1.set_title('New York Temperature, Google, and Yahoo!', fontsize=22)
ax1.set_xlabel('Date (MJD)')
ax1.set_xlim(48800, 55610)
ax1.set_ylabel('Value (Dollars)')
ax1.set_ylim(-20, 770)
ax2.set_ylabel(r'Temperature $^\circ$F')
ax2.set_ylim(-150, 100)
# Create Legend
handles = []
lables = []
for axis in (ax1, ax2):
  handle, label = axis.get_legend_handles_labels()
  for i in range(0,len(handle)):
    handles.append(handle[i])
    labels.append(label[i])
handles[1], handles[2] = handles[2], handles[1]
ax1.legend(handles, labels, loc=6, frameon=False)
# Set minor ticks
xminorLocator = MultipleLocator(200)
y1minorLocator = MultipleLocator(20)
y2minorLocator = MultipleLocator(10)
ax1.xaxis.set_minor_locator(xminorLocator)
ax1.yaxis.set_minor_locator(y1minorLocator)
ax2.yaxis.set_minor_locator(y2minorLocator)
# Get rid of ticks on top
ax1.xaxis.set_ticks_position('bottom')
