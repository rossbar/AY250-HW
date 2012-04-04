import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# Load the data
filename = 'randomData.txt'
coord = np.dtype(dict(names=('x', 'y', 'z'), \
                      formats=('float', 'float', 'float') ) )
data = np.loadtxt(filename, dtype=coord, delimiter=',')

# create the subplots
f, axs = plt.subplots(2,2)
axs[0][0].plot(data['x'], data['y'], 'bo')
axs[0][0].set_title('Blue Data')
axs[0][1].plot(data['x'], data['z'], 'ro')
axs[0][1].set_title('Red Data')
axs[1][0].plot(data['y'], data['z'], 'go')
axs[1][0].set_title('Green Data')
axs[1][1].plot(data['x'], data['y'], 'bo', data['y'], data['z'], 'ro', \
               data['x'], data['z'], 'go' )
axs[1][1].set_title('All Data')

rect = Rectangle( (.219,.223), .3, .3, fill=False)
axs[1][1].add_patch(rect)
f.canvas.draw()
# Start messing with mpl
# def onclick(event):
#   print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' \
#         %(event.button, event.x, event.y, event.xdata, event.ydata )
# 
# def onrelease(event):
#   print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' \
#         %(event.button, event.x, event.y, event.xdata, event.ydata )
#   
#  def getDataCoord(event):
#    return event.xdata, event.ydata
#  
#  cid = f.canvas.mpl_connect('button_press_event', getDataCoord)
#  cjd = f.canvas.mpl_connect('button_release_event', getDataCoord)

class rect:

  def __init__(self, axisObj, figure):
    self.figure = figure
    self.connect()    

  def connect(self):
    self.cidpress = self.figure.canvas.mpl_connect('button_press_event',\
                    self.onPress)
    self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', \
                      self.onRelease)
  def onPress(self, event):
    self.x, self.y, self.datax, self.datay = event.x, event.y, event.xdata, \
                                             event.ydata

  def onRelease(self, event):
    self.h = event.y - self.y
    self.w = event.x - self.x

  def drawRect(self):
    self.rect = Rectangle( (self.x, self.y), self.w, self.h, fill=False )
    axisObj.add_patch(self.rect)
    fig.canvas.draw()

R = rect(axs[1][1], f)
R.drawRect()
